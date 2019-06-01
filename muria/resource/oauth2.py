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

"""OAuth2 Resource."""

import falcon
import base64
from pony.orm import db_session
from muria.init import config, tokenizer
from muria.resource.base import Resource
from muria.db.schema import Login_Schema
from muria.db.model import Pengguna
from muria.lib.misc import dumpAsJSON


def get_basic_auth(request, content_type="application/x-www-form-urlencoded"):
    """Extract Auth Basic from user request."""
    req = request
    if req.content_type == content_type and req.headers.get("AUTHORIZATION"):
        basic = req.headers.get("AUTHORIZATION", "").partition("Basic ")[2]
        return bytes(basic, "utf-8")


def decode_basic_auth(string):
    """Decode string with base64."""
    if not isinstance(string, bytes):
        string = bytes(string, "utf-8")

    basic = base64.decodebytes(string).decode("utf-8")
    username, sep, password = basic.partition(":")
    return username, password


class Oauth2(Resource):
    """Oauth2 Resource."""

    def on_get(self, req, resp, **params):
        """Test method, a la ping."""
        data = req.media
        print(data)
        resp.status = falcon.HTTP_OK
        resp.set_header("WWW-Authenticate", "Bearer")
        content = {"WWW-Authenticate": "Bearer"}
        resp.body = dumpAsJSON(content)

    @db_session
    def on_post(self, req, resp, **params):

        if not config.getboolean("security", "secure"):
            raise falcon.HTTPBadRequest(
                title="HTTPS Required",
                description=(
                    "All requests must be performed via the HTTPS protocol. "
                    "Please switch to HTTPS and try again."
                ),
            )
        # TODO: Need to implement client_id and client_secret instead of
        #       using username and password credentials directly as of
        #       swagger-editor send Auth Basic in client_id
        #       and client_secret pair
        auth_basic = get_basic_auth(req, "application/x-www-form-urlencoded")
        if auth_basic is not None:
            user, password = decode_basic_auth(auth_basic)
            credentials = {"username": user, "password": password}
        else:
            credentials = req.media

        print(credentials)

        data, errors = Login_Schema().load(credentials)
        if errors:
            # entity is received but unable to process, may due to:
            # blank entity, or invalid one.
            raise falcon.HTTPUnprocessableEntity(
                description=str(errors), code=422
            )

        if not Pengguna.exists(username=data["username"]):
            raise falcon.HTTPUnauthorized(code=401)

        auth_user = Pengguna.get(username=data["username"])

        if auth_user.checkPassword(data["password"]):

            token_payload = {
                "name": auth_user.orang.nama,
                "pid": str(auth_user.orang.id),
                "roles": [x for x in auth_user.kewenangan.wewenang.nama],
            }
            print(token_payload, data["password"])

            tokens = tokenizer.createAccessToken(token_payload)

            if tokens is None:
                # unable to create token
                raise falcon.HTTPInternalServerError(code=500)

            content = {
                # some clients do not recognize the token type if
                # not properly titled case as in RFC6750 section-2.1
                "token_type": "Bearer",
                "expires_in": self.config.getint(
                    "security", "access_token_exp"
                ),
                "refresh_token": tokens["refresh_token"],
                "access_token": tokens["access_token"],
            }
            resp.status = falcon.HTTP_OK
            resp.body = dumpAsJSON(content)
        else:
            # entity is received but not authorized by the server
            # due to invalid credentials.
            raise falcon.HTTPUnauthorized(code=401)
