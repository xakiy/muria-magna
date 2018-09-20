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
import falcon
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

    def hashPassword(self, text):
        """ Hash password menyerupai MySQL password() bekerja,
        select sha1(unhex(sha1('text'))) """
        hex_digested = hashlib.sha1(bytes(text, 'utf8')).hexdigest()
        hashed_bin = binascii.unhexlify(hex_digested)
        hashed = hashlib.sha1(hashed_bin).hexdigest()
        return hashed

    def isToken(self, token):
        if isinstance(token, str) and token.count('.') == 2:
            return True
        else:
            return False

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
                'exp': now + timedelta(seconds=self.access_token_exp)
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
        if self.isToken(access_token):
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
                raise falcon.HTTPNotFound(
                    title='Token Verification',
                    description=str(err),
                    code={'error_code': 4003}
                )
        else:
            raise falcon.HTTPNotFound(
                title='Token Verification',
                description='Invalid content',
                code={'error_code': 4001}
            )

    def refreshAccessToken(self, access_token, refresh_token):
        if self.isToken(access_token) and self.isToken(refresh_token):
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
                raise falcon.HTTPNotFound(
                    title='Token Verification',
                    description=str(err),
                    code={'error_code': 4003}
                )
            else:
                try:
                    refresh_payload = jwt.decode(
                        refresh_token,
                        key=self.public_key,
                        algorithms=self.algorithm,
                        issuer=self.token_issuer,
                        audience=self.token_audience
                    )
                except jwt.ExpiredSignatureError as err:
                    raise falcon.HTTPNotFound(
                        title='Refresh Token Expired',
                        description=str(err),
                        code={'error_code': 5002}
                    )
                else:
                    if acc_token_sig == refresh_payload['tsig']:
                        return self.createAccessToken(token_payload)
                    else:
                        raise falcon.HTTPNotFound(
                            title='Token Refresh',
                            description='Token pair mismatch',
                            code={'error_code': 4005}
                        )
        else:
            raise falcon.HTTPNotFound(
                title='Token Refresh',
                description='Invalid content',
                code={'error_code': 4001}
            )
