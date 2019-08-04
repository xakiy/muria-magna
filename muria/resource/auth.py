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

"""Auth Resource."""

import falcon
from muria.init import DEBUG, tokenizer
from muria.resource.base import Resource
from muria.db.schema import Login_Schema, Pengguna_Schema
from muria.db.model import Pengguna

from pony.orm import db_session


class Authentication(Resource):
    """
    Resource Authentication

    Menangani otentifikasi pengguna, termasuk yang mengeluarkan jwt.
    """

    @db_session
    def on_get(self, req, resp):

        resp.status = falcon.HTTP_OK
        resp.set_header("WWW-Authenticate", "Bearer")
        if DEBUG:
            content = {"WWW-Authenticate": "Bearer"}
            resp.media = content

    @db_session
    def on_post(self, req, resp):
        data, errors = Login_Schema().load(req.media)
        if errors:
            # entity is received but unable to process, may due to:
            # blank entity, or invalid one.
            raise falcon.HTTPUnprocessableEntity(description=str(errors), code=422)

        if not Pengguna.exists(username=data["username"]):
            raise falcon.HTTPUnauthorized(code=401)

        auth_user = Pengguna.get(username=data["username"])

        if auth_user.checkPassword(data["password"]):

            token_payload = {
                "name": auth_user.orang.nama,
                "pid": str(auth_user.orang.id),
                "roles": [x for x in auth_user.kewenangan.wewenang.nama],
            }

            tokens = tokenizer.createAccessToken(token_payload)

            if tokens is None:
                # unable to create token
                raise falcon.HTTPInternalServerError(code=500)

            content = {
                # some clients do not recognize the token type if
                # not properly titled case as in RFC6750 section-2.1
                "token_type": "Bearer",
                "expires_in": self.config.getint("security", "access_token_exp"),
                "refresh_token": tokens["refresh_token"],
                "access_token": tokens["access_token"],
            }
            resp.status = falcon.HTTP_OK
            resp.media = content
        else:
            # entity is received but not authorized by the server
            # due to invalid credentials.
            raise falcon.HTTPUnauthorized(code=401)


class Verification(Resource):
    """
    Resource Verification

    Memverifikasi jwt yang dikirimkan oleh klien
    """

    def on_post(self, req, resp, **params):

        access_token = req.media.get("access_token")

        # TODO:
        # implement some cache validations on the user
        token = tokenizer.verifyAccessToken(access_token)

        if tokenizer.isToken(token):
            content = {"access_token": token}
            resp.status = falcon.HTTP_200
            resp.media = content

        elif token[0] == 422:
            raise falcon.HTTPUnprocessableEntity(
                title="Token Verification", description=str(token[1]), code=422
            )
        else:
            raise falcon.HTTPBadRequest(
                title="Token Verification", description=str(token[1]), code=400
            )


class Refresh(Resource):
    def on_post(self, req, resp, **params):

        access_token = req.media.get("access_token")
        refresh_token = req.media.get("refresh_token")

        # on success it will be dict of tokens, otherwise it will
        # tuple of error
        content = tokenizer.refreshAccessToken(access_token, refresh_token)

        if isinstance(content, dict):
            payload = {
                "token_type": "Bearer",
                "expires_in": self.config.getint("security", "access_token_exp"),
                "refresh_token": content["refresh_token"],
                "access_token": content["access_token"],
            }
            resp.status = falcon.HTTP_OK
            resp.media = payload
        # tuple of error
        elif content[0] == 422:
            raise falcon.HTTPUnprocessableEntity(
                title="Renew Access Token", description=str(content[1]), code=422
            )
        elif content[0] == 432:
            raise falcon.HTTPUnprocessableEntity(
                title="Renew Refresh Token Expired",
                description=str(content[1]),
                code=432,
            )
        else:
            raise falcon.HTTPBadRequest(
                title="Renew Tokens Pair", description=str(token[1]), code=400
            )
