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
        print('AUTH GET: ', req)
        resp.status = falcon.HTTP_200
        if DEBUG:
            content = {'username': 'your username', 'password': 'your password'}
            resp.body = libs.dumpAsJSON(content)

    @db_session
    def on_post(self, req, resp):
        print('AUTH POST: ', req, req.media)
        # any invalid JSON would be cought within falcon's
        # req.media deserialization
        if req.media:
            ps = Pengguna_Schema()
            auth_user, error = ps.load(req.media)

            if error:
                # entity is received but unable to process, may due to:
                # blank entity, or invalid one.
                raise falcon.HTTPUnprocessableEntity(code=422)


            if isinstance(auth_user, Pengguna):

                token_payload = {
                    'name': auth_user.orang.nama,
                    'pid': auth_user.orang.id.hex,
                    'roles': [ x for x in auth_user.kewenangan.wewenang.nama ]
                }

                tokens = tokenizer.createAccessToken(token_payload)

                if tokens is None:
                    # unable to create token
                    raise falcon.HTTPInternalServerError(code=500)

                content = {
                    'token_type': 'bearer',
                    'expires_in': self.config.getint('security', 'access_token_exp'),
                    'refresh_token': tokens['refresh_token'],
                    'access_token': tokens['access_token']
                }
                resp.status = falcon.HTTP_OK
            else:
                # entity is received but not authorized by the server
                # due to invalid credentials.
                 raise falcon.HTTPUnauthorized(code=401)

            resp.body = libs.dumpAsJSON(content)


class Verification(Resource):
    """
    Resource Verification

    Memverifikasi jwt yang dikirimkan oleh klien
    """

    def on_post(self, req, resp, **params):

        access_token = req.media.get('access_token')

        # TODO:
        # implement some cache validations on the user
        token = tokenizer.verifyAccessToken(access_token)

        if tokenizer.isToken(token):
            content = {"access_token": token}
            resp.status = falcon.HTTP_200
            resp.body = libs.dumpAsJSON(content)

        elif token[0] == 422:
            raise falcon.HTTPUnprocessableEntity(
                title='Token Verification',
                description=str(token[1]), code=422)
        else:
            raise falcon.HTTPBadRequest(
                title='Token Verification',
                description=str(token[1]), code=400)


class Refresh(Resource):

    def on_post(self, req, resp, **params):

        access_token = req.media.get('access_token')
        refresh_token = req.media.get('refresh_token')

        tokens = tokenizer.refreshAccessToken(access_token, refresh_token)

        if isinstance(tokens, dict):
            content = {
                'token_type': 'bearer',
                'expires_in': self.config.getint('security', 'access_token_exp'),
                'refresh_token': tokens['refresh_token'],
                'access_token': tokens['access_token']
            }
            resp.status = falcon.HTTP_OK
            resp.body = libs.dumpAsJSON(content)

        elif tokens[0] == 422:
            raise falcon.HTTPUnprocessableEntity(
                title='Renew Access Token',
                description=str(tokens[1]), code=422)
        elif tokens[0] == 432:
            raise falcon.HTTPUnprocessableEntity(
                title='Renew Refresh Token Expired',
                description=str(tokens[1]), code=432)
        else:
            raise falcon.HTTPBadRequest(
                title='Renew Tokens Pair',
                description=str(token[1]), code=400)

