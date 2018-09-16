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
"""Init env dan konfigurasi lainnya."""

from muria.lib.config import Parser
from muria.conf.policy import Policy_Config
from muria.db.manager import DBManager


# Middlewares
# from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
# from falcon_jwt_checker import JwtChecker

from falcon_cors import CORS
from falcon_multipart.middleware import MultipartMiddleware
from muria.middleware.jwt_checker import GiriJwtChecker
from muria.middleware.rbac import RBAC
from muria.lib.tokenizer import Tokenizer
from muria.lib.logger import Logger


# MURIA_SETUP merupakan env yang menunjuk ke berkas
# konfigurasi produksi atau pengembangan.
# seperti: export MURIA_SETUP=~/config/devel.ini
config = Parser(setup='MURIA_SETUP')

DEBUG = config.getboolean('app', 'debug')

connection = DBManager(config)  # database connection

from muria.conf import premise

premise.setPremise()

tokenizer = Tokenizer(config)
logger = Logger(config)

middleware_list = []

if config.getboolean('security', 'secure'):

    cors = CORS(
        log_level=10,
        # allow_all_origins=False,  # false means disallow any random host to connect
        allow_origins_list=config.getlist('cors', 'allow_origins_list'),
        allow_all_methods=True,  # whether all methods are allowed via CORS requests
        # allow_methods_list=['GET', 'POST', 'TRACE', 'PUT', 'PATCH', 'HEAD', 'CONNECT', 'DELETE', 'OPTIONS'],
        # exposed value sent as response to the Access-Control-Expose-Headers request
        expose_headers_list=['HEAD', 'GET', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allow_all_headers=True,  # preflight response
        allow_headers_list=['HEAD', 'GET', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allow_credentials_all_origins=True,
        allow_credentials_origins_list=[],
        # max_age=None
        # TODO: move these values to config file
    )

    jwt_checker = GiriJwtChecker(
        secret=config.getbinary('security', 'public_key'),  # May be a public key
        algorithm=config.get('security', 'algorithm'),
        issuer=config.get('security', 'issuer'),
        audience=config.get('security', 'audience'),
        leeway=60,
        exempt_routes=[
            # excluded routes
            '/auth',
            '/auth/verify',
            '/auth/refresh',
            '/upload'
        ],
        exempt_methods=[
            # excluded HTTP methods
            'OPTIONS'
        ]
    )

    middleware_list.append(cors.middleware)
    middleware_list.append(jwt_checker)
    middleware_list.append(RBAC(Policy_Config, check_jwt=True))

middleware_list.append(MultipartMiddleware())
