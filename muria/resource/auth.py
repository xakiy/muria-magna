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
import datetime
from muria.init import DEBUG
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

        if req.media:
            ps = Pengguna_Schema()
            auth_user, error = ps.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_BAD_REQUEST,
                                       title='Invalid Parameters',
                                       code=error)
            '''
            JWT Reserved Claims
            Claims    name          Format         Usage
            -------   ----------    ------         ---------
            ‘exp’     Expiration    int            The time after which the token is invalid.
            ‘nbf’     Not before    int            The time before which the token is invalid.
            ‘iss’     Issuer        str            The principal that issued the JWT.
            ‘aud’     Audience      str/list(str)  The recipient that the JWT is intended for.
            ‘iat’     Issued At     int            The time at which the JWT was issued.
            '''
            if isinstance(auth_user, Pengguna):
                payload = {
                    'name': auth_user.orang.nama,
                    'pid': auth_user.orang.id.hex,
                    'roles': auth_user.wewenang.nama,
                    'iss': self.config.get('security', 'issuer'),
                    'aud': self.config.get('security', 'audience'),
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
                }

                # Buat token
                token = jwt.encode(
                    payload,
                    self.config.getbinary('security', 'private_key'),
                    algorithm=self.config.get('security', 'algorithm')
                )

                content = {'token': token}
                resp.status = falcon.HTTP_OK
            else:
                content = {'message': 'Authentication failed'}
                resp.status = falcon.HTTP_UNAUTHORIZED

            resp.body = libs.dumpAsJSON(content)

        else:
            raise falcon.HTTP_BAD_REQUEST(
                title='Invalid JSON',
                description='Could not decode the request body. The JSON was incorrect.'
            )

    def on_options(self, req, resp):

        resp.status = falcon.HTTP_OK


class Verification(Resource):
    """
    Resource Verification

    Memverifikasi jwt yang dikirimkan oleh klien
    """

    @db_session
    def on_get(self, req, resp, **params):

        token = req.get_param('token')

        try:
            payload = jwt.decode(
                token,
                key=self.config.getbinary('security', 'public_key'),
                algorithm=self.config.get('security', 'algorithm'),
                issuer=self.config.get('security', 'issuer'),
                audience=self.config.get('security', 'audience')
            )
            content = {"token": token}
            resp.status = falcon.HTTP_200
            resp.body = libs.dumpAsJSON(content)

        except jwt.InvalidTokenError as err:
            raise falcon.HTTPNotFound(description=str(err))


class Refresh(Resource):

    def on_get(self, req, resp, **params):
        pass

    def on_post(self, req, resp, **params):
        pass
