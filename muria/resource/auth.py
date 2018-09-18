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

"""muria auth class file."""

import falcon
import jwt
from muria.init import DEBUG, tokenizer
from muria.resource.base import Resource
from muria.schema.entity import Pengguna_Schema
from muria.db.model import Pengguna
from muria import libs

from pony.orm import db_session


class Authentication(Resource):
    """
    Resource Authentication

    Menangani otentifikasi pengguna, termasuk yang mengeluarkan jwt.
    """

    @db_session
    def on_get(self, req, resp):

        resp.status = falcon.HTTP_200
        if DEBUG:
            content = {'username': 'your username', 'password': 'your password'}
            resp.body = libs.dumpAsJSON(content)

    @db_session
    def on_post(self, req, resp):
        # any invalid JSON would be cought within falcon's
        # req.media deserialization
        if req.media:
            ps = Pengguna_Schema()
            auth_user, error = ps.load(req.media)

            if error:
                raise falcon.HTTPError(
                    falcon.HTTP_BAD_REQUEST,
                    title='Invalid Params',
                    code=error)

            if isinstance(auth_user, Pengguna):

                token_payload = {
                    'name': auth_user.orang.nama,
                    'pid': auth_user.orang.id.hex,
                    'roles': auth_user.wewenang.nama
                }

                tokens = tokenizer.createAccessToken(token_payload)

                content = {
                    'token_type': 'bearer',
                    'expires_in': self.config.getint('security', 'access_token_exp'),
                    'refresh_token': tokens['refresh_token'],
                    'access_token': tokens['access_token']
                }
                resp.status = falcon.HTTP_OK
            else:
                content = {'message': 'Authentication failed'}
                resp.status = falcon.HTTP_UNAUTHORIZED

            resp.body = libs.dumpAsJSON(content)

    def on_options(self, req, resp):

        resp.status = falcon.HTTP_OK


class Verification(Resource):
    """
    Resource Verification

    Memverifikasi jwt yang dikirimkan oleh klien
    """

    @db_session
    def on_post(self, req, resp, **params):

        print('#DEBUG @auth/verify')
        # DEBUG
        print('headers: ', req.headers)
        print('acc_route: ', req.access_route)
        # print('params: ', req.params)
        print('media: ', req.media)

        access_token = req.media.get('access_token')

        try:
            # TODO:
            # implement some cache validations on the user
            jwt.decode(
                access_token,
                key=self.config.getbinary('security', 'public_key'),
                algorithms=self.config.get('security', 'algorithm'),
                issuer=self.config.get('security', 'issuer'),
                audience=self.config.get('security', 'audience')
            )
            content = {"access_token": access_token}
            resp.status = falcon.HTTP_200
            resp.body = libs.dumpAsJSON(content)

        except jwt.InvalidTokenError as err:
            raise falcon.HTTPNotFound(
                title='Token Verification',
                description=str(err), code={'error_code': 4003}
            )


class Refresh(Resource):

    def on_post(self, req, resp, **params):

        access_token = req.media.get('access_token')
        refresh_token = req.media.get('refresh_token')

        tokens = tokenizer.refreshAccessToken(access_token, refresh_token)

        content = {
            'token_type': 'bearer',
            'expires_in': self.config.getint('security', 'access_token_exp'),
            'refresh_token': tokens['refresh_token'],
            'access_token': tokens['access_token']
        }
        resp.status = falcon.HTTP_OK
        resp.body = libs.dumpAsJSON(content)
