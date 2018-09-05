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

from conf.policy import Policy_Config
from db.manager import DBManager

# Middlewares
# from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
# from falcon_jwt_checker import JwtChecker
from muria.jwt_checker import GiriJwtChecker as JwtChecker
from falcon_cors import CORS
from falcon_policy import RoleBasedPolicy
from falcon_multipart.middleware import MultipartMiddleware
from lib.config import Config


# MURIA_SETUP merupakan env yang menunjuk ke berkas
# konfigurasi produksi atau pengembangan.
# seperti: export MURIA_SETUP=~/config/devel.ini
config = Config(setup='MURIA_SETUP')

DEBUG = config.getboolean('app', 'debug')

connection = DBManager(config)  # database connection

from db import premise

middleware_list = []

if config.getboolean('security', 'secure'):

    cors = CORS(
        # log level
        # DEBUG = 10
        # INFO = 20
        # WARN/WARNING = 30
        # ERROR = 40
        # CRITICAL/FATAL = 50
        log_level = 10,
        # allow_all_origins=True,
        allow_origins_list=['api.krokod.net'], # config.getlist('cors', 'allow_origins_list'),
        # allow_methods_list=config.getlist('cors', 'allow_methods_list'),
        # allow_all_methods=True,
        # expose_headers_list=['GET', 'OPTIONS', 'POST', 'HEAD', 'PUT', 'DELETE'],
        # allow_all_headers=True
    )

    jwt_checker = JwtChecker(
        secret=config.getbinary('security', 'public_key'),  # May be a public key
        algorithm=config.get('security', 'algorithm'),
        issuer=config.get('security', 'issuer'),
        audience=config.get('security', 'audience'),
        leeway=30,
        exempt_routes=[
            # excluded routes
            '/auth',
            '/upload'
        ],
        exempt_methods=[
            # excluded HTTP methods
            'OPTIONS'
        ]
    )

    middleware_list.append(cors.middleware)
    middleware_list.append(jwt_checker)
    middleware_list.append(RoleBasedPolicy(Policy_Config, check_jwt=True))

middleware_list.append(MultipartMiddleware())
