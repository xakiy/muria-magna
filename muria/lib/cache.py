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
Cache Class

Menyimpan data-data temporal dalam bentuk key/value.
Implementasi cache tergantung ketersediaan infrastruktur,
bisa Redis atau Memcache.
"""

from init import config


class Cache(object):

    def __init__(self):
        self.cache_engine = config.get('cache', 'engine')
        if cache_engine == 'memcache':
            from pymemcache.client import base
            self.client = base.Client(('localhost', 11211))
            try:
                self.client._connect()
            except ConnectionRefusedError as err:
                print(err)
                return False
            return True
        elif cache_engine == 'redis':
            pass



    def set(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.set(key)

    def del(self, key):
        return self.client.delete(key)
