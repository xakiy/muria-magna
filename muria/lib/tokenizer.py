"""muria tokenizer file."""

# Copyright 2017 Ahmad Ghulam Zakiy <ghulam (dot) zakiy (at) gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jwt
import hashlib
import binascii
from os import urandom
from datetime import datetime, timedelta
from calendar import timegm


class Tokenizer(object):

    def __init__(self, config, ecdsa=True, rsa=False):

        self.private_key = config.getbinary('security', 'private_key')
        self.public_key = config.getbinary('security', 'public_key')
        self.algorithm = config.get('security', 'algorithm')
        self.token_issuer = config.get('security', 'issuer')
        self.token_audience = config.get('security', 'audience')
        self.access_token_exp = config.getint('security', 'access_token_exp')
        self.refresh_token_exp = config.getint('security', 'refresh_token_exp')

    def createSaltedPassword(self, digest):
        """Create new password based on supplied digest.
        Args:
            digest (hex hashed string): sha256 hashed string in hex mode.
        Return tuple of hex version of the salt and new password.
        """

        salt_bin = urandom(20)
        hashed_bin = hashlib.sha256(bytes(digest, 'utf8')).digest()
        hashed_bin_key = hashlib.pbkdf2_hmac('sha256', hashed_bin, salt_bin, 1000)
        return (salt_bin.hex(), hashed_bin_key.hex())

    def getSaltedPassword(self, salt, digest):
        salt_bin = binascii.unhexlify(salt)
        hashed_bin = hashlib.sha256(bytes(digest, 'utf8')).digest()
        hashed_bin_key = hashlib.pbkdf2_hmac('sha256', hashed_bin, salt_bin, 1000)
        return hashed_bin_key.hex()

    def isToken(self, token):
        return isinstance(token, str) and token.count('.') == 2

    def createAccessToken(self, payload):

        '''
        JWT Reserved Claims
        Claims    name          Format         Usage
        -------   ----------    ------         ---------
        ‘exp’     Expiration    int            The time after which the token is invalid.
        ‘nbf’     Not before    int            The time before which the token is invalid.
        ‘iss’     Issuer        str            The principal that issued the JWT.
        ‘aud’     Audience      str/list(str)  The recipient that the JWT is intended for.
        ‘iat’     Issued At     int            The time at which the JWT was issued.

        The time values will be converted automatically into int if it populated with datetime object.
        '''

        if isinstance(payload, dict):
            tokens = dict()
            now = datetime.utcnow()
            access_token_default_claims = {
                'iss': self.token_issuer,
                'aud': self.token_audience,
                'iat': now,
                'exp': now + timedelta(seconds=self.access_token_exp),
            }
            access_token_payload = payload.copy()
            access_token_payload.update(access_token_default_claims)

            tokens['access_token'] = jwt.encode(
                access_token_payload,
                self.private_key,
                algorithm=self.algorithm
            )

            acc_token_sig = bytes(tokens['access_token']).decode('utf8').split('.')[2]

            refresh_token_payload = {
                'tsig': acc_token_sig,
                # decode this unixtimestamp using datetime.utcfromtimestamp()
                'tiat': timegm(now.utctimetuple()),
                'iss': self.token_issuer,
                'aud': self.token_audience,
                'iat': now,
                'exp': now + timedelta(seconds=self.refresh_token_exp)
            }
            tokens['refresh_token'] = jwt.encode(
                refresh_token_payload,
                self.private_key,
                algorithm=self.algorithm
            )
            return tokens
        else:
            return None

    def verifyAccessToken(self, access_token):
        if not self.isToken(access_token):
            return (400, 'Bad Token')

        try:
            jwt.decode(
                access_token,
                key=self.public_key,
                algorithms=self.algorithm,
                issuer=self.token_issuer,
                audience=self.token_audience,
            )
            return access_token
        except jwt.InvalidTokenError as err:
            # token is received but unable to process due to
            # invalid content or invalid signature
            return (422, err)

    def refreshAccessToken(self, access_token, refresh_token):
        # on success this will return pair of refreshed
        # access token and refresh token, otherwise it
        # will return tuple of error code

        if not self.isToken(access_token) or not self.isToken(refresh_token):
            return (400, 'Bad Tokens Pair')

        acc_token_sig = access_token.split('.')[2]
        try:
            token_payload = jwt.decode(
                access_token,
                key=self.public_key,
                algorithms=self.algorithm,
                issuer=self.token_issuer,
                audience=self.token_audience,
                options={'verify_exp': False}
            )
        except jwt.InvalidTokenError as err:
            return (422, err)

        try:
            refresh_payload = jwt.decode(
                refresh_token,
                key=self.public_key,
                algorithms=self.algorithm,
                issuer=self.token_issuer,
                audience=self.token_audience
            )
        except jwt.ExpiredSignatureError as err:
            return (432, err)

        if acc_token_sig == refresh_payload['tsig']:
            return self.createAccessToken(token_payload)
        else:
            return (400, 'Token Pair Mismatch')
