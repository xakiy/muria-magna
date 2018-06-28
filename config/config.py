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
"""muria config class."""

import os

class Configuration(object):

    def __init__(self, base_dir):
        print(base_dir, '@config')
        self.directory = {
            'base_dir': base_dir,
            'pub_dir': 'pub/'
        }

        self.application = {
            'debug': True,
            'page_limit': 1000,
            'create_table': True
        }

        self.database = {
            'engine': 'mysql',  # bisa sqlite, postgresql, atau oracle'''
            'host': 'localhost',
            'user': 'muria',
            'password': 't4tt4r4t4',
            'port': 3306,
            'database': 'db_muria'
        }

        try:
            ssl_path = os.path.join(self.path('base_dir'), 'config', 'ssl')
            private = open(
                os.path.join(ssl_path, 'ecdsa_private_key.pem'), 'rb').read()
            public = open(
                os.path.join(ssl_path, 'ecdsa_public_key.pem'), 'rb').read()

            self.security = {
                # Enkripsi yang dipakai, bisa ES256(ECDSA 256bit)/RS256 ke atas
                'algorithm': 'ES256',
                'private_key': private,
                'public_key': public,
                'secure': True,
                'cors_allow_all_origins': True,
                'cors_allow_origins_list': [
                    'http://localhost:8000',
                    'http://www.krokod.net',
                    'http://api.krokod.net']}

        except IOError as err:
            print('Something bad happen: {error}'.format(error=err))

    def app(self, prop):
        return self.application.get(prop)

    def db(self, prop):
        return self.database.get(prop)

    def sec(self, prop):
        return self.security.get(prop)

    def path(self, prop):
        return self.directory.get(prop)
