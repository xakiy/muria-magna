import os
from config.config import Configuration
from config.policy import Policy_Config
from muria.database import Connection

## Middlewares
# from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
#from falcon_jwt_checker import JwtChecker
from muria.jwt_checker import GiriJwtChecker as JwtChecker
from falcon_cors import CORS
from falcon_policy import RoleBasedPolicy
from falcon_multipart.middleware import MultipartMiddleware

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

#print(__file__)
#print(os.path.abspath(__file__))
print(BASE_DIR, CONFIG_DIR)

config = Configuration(BASE_DIR)  # global config
connection = Connection(config)  # database connection

middleware_list = []

if config.sec('secure'):

    cors = CORS(
        #allow_all_origins=True,
        allow_origins_list=config.sec('cors_allow_origins_list'),
        allow_methods_list=['GET', 'OPTIONS', 'POST', 'HEAD', 'PUT', 'DELETE'],
        #allow_all_methods=True,
        #expose_headers_list=['GET', 'OPTIONS', 'POST', 'HEAD', 'PUT', 'DELETE'],
        allow_all_headers=True)

    jwt_checker = JwtChecker(
        secret=config.sec('public_key'),  # May be a public key
        algorithm=config.sec('algorithm'),
        # Routes listed here will not require a JWT
        exempt_routes=['/auth', '/upload'],
        exempt_methods=[
            'OPTIONS'
        ],  # HTTP request methods listed here will not require a jwt
        # audience='www.krokod.net',
        leeway=30)

    middleware_list.append(jwt_checker)
    middleware_list.append(RoleBasedPolicy(Policy_Config))
    middleware_list.append(cors.middleware)

middleware_list.append(MultipartMiddleware())
