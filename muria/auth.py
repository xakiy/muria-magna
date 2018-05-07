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

from muria.schema import User_Schema
from muria.entities import User
from muria import libs

from pony.orm import db_session
from falcon_cors import CORS


class Authentication(object):
    """Resource Authentication

    Menangani otentifikasi pengguna, termasuk yang mengeluarkan jwt.
    """

    def __init__(self, config):
        self.config = config
        self.cors = CORS(
            allow_origins_list=self.config.sec('cors_allow_origins_list'),
            allow_all_headers=True,
            allow_all_methods=True)

    @db_session
    def on_get(self, req, resp):

        content = {'username': 'your username', 'password': 'your password'}
        resp.status = falcon.HTTP_200
        resp.body = libs.dumpAsJSON(content)

    @db_session
    def on_post(self, req, resp):

        print('#DEBUG @auth')
        # DEBUG
        print('headers: ', req.headers)
        print('acc_route: ', req.access_route)
        print('params: ', req.params)
        print('media: ', req.media)

        if req.media:
            us = User_Schema()
            auth_user, error = us.load(req.media)
            #print(user)

            if error:
                raise falcon.HTTPError(falcon.HTTP_BAD_REQUEST,
                                       title='Invalid Parameters',
                                       code=error)

            if isinstance(auth_user, User):
                # Isi payload
                payload = {
                    'name': str(auth_user.pid.nama),
                    'pid': str(auth_user.pid.id),
                    'roles': str('admin')
                    # iss: issuer
                    # iat: issued at
                }

                # Buat token
                token = jwt.encode(
                    payload,
                    self.config.sec('private_key'),
                    algorithm=self.config.sec('algorithm')
                )

                content = {'token': token}
                resp.status = falcon.HTTP_OK
            else:
                content = {'message': 'Authentication failed'}
                resp.status = falcon.HTTP_UNAUTHORIZED
        else:
            raise falcon.HTTPError(
                falcon.HTTP_BAD_REQUEST,
                'Invalid JSON',
                'Could not decode the request body. The JSON was incorrect.'
            )

        resp.body = libs.dumpAsJSON(content)

    def on_options(self, req, resp):

        resp.status = falcon.HTTP_OK


class Verification(object):
    """Resource Verification
    Memverifikasi jwt yang dikirimkan oleh klien
    """

    def __init__(self, config):
        self.config = config
        self.cors = CORS(
            allow_origins_list=self.config.sec('cors_allow_origins_list'),
            allow_all_headers=True,
            allow_all_methods=True)

    @db_session
    def on_get(self, req, resp, **params):

        # DEBUG
        print('#DEBUG')
        print(req.headers)
        print(req.access_route)
        print(req.params)

        token = req.get_header('Authorization').split(' ')[1]
        print(token)

        payload = jwt.decode(
            token,
            self.config.sec('public_key'),
            self.config.sec('algorithm')
        )
        print(payload)
        # BUG
        # Need sanity check!
        auth_user = User.get(pid=payload['pid'])

        if auth_user is not None:
            print('#TEST', payload)
            content = {"token": token}
            resp.status = falcon.HTTP_200
        else:
            content = {"errot": 'Token invalid'}
            resp.status = falcon.HTTP_404

        resp.body = libs.dumpAsJSON(content)
