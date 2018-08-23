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
"""
Init

Inisialisasi lingkungan dan berbagai konfigurasi
"""

import os
from configparser import ConfigParser, ExtendedInterpolation
from conf.policy import Policy_Config
from muria.database import Connection

# Middlewares
# from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
# from falcon_jwt_checker import JwtChecker
from muria.jwt_checker import GiriJwtChecker as JwtChecker
from falcon_cors import CORS
from falcon_policy import RoleBasedPolicy
from falcon_multipart.middleware import MultipartMiddleware

# ConfigParser modified
class Config(ConfigParser):
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)

    def getlist(self, section, option, delim=' ', **kwargs):
        return self.get(section, option, **kwargs).split(delim)

    def getbinary(self, section, option, **kwargs):
        return bytes(self.get(section, option, **kwargs), 'utf8')

config = Config(interpolation=ExtendedInterpolation())
if os.path.isdir(str(os.environ.get('MURIA_CONFIG_PATH'))):
    config_file = os.path.join(os.environ['MURIA_CONFIG_PATH'], 'muria.ini')
else:
    raise EnvironmentError('MURIA_CONFIG_PATH belum diset!')

if not bool(config.read(config_file).count(config_file)):
    raise FileNotFoundError('File konfigurasi %s tidak ditemukan' % config_file)

app_path = os.path.dirname(os.path.abspath(__file__))

config.set('path', 'base_dir', app_path)
config.set('path', 'config_dir', os.environ['MURIA_CONFIG_PATH'])

priv_key = config.get('security', 'private_key')
pub_key = config.get('security', 'public_key')

if os.path.isfile(priv_key) and os.path.isfile(pub_key):
    config.set('security', 'private_key', open(priv_key, 'r').read())
    config.set('security', 'public_key', open(pub_key, 'r').read())
else:
    raise FileNotFoundError('File SSL tidak ditemukan!')

DEBUG = config.getboolean('app', 'debug')

connection = Connection(config)  # database connection

middleware_list = []

if config.getboolean('security', 'strict'):

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
        secret=config.get('security', 'public_key'),  # May be a public key
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
