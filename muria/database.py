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

""" muria Connection class """

from pony.orm import Database, sql_debug

class Connection(object):
    def __init__(self, config):
        self.config = config

        # tanpa try-except untuk menampakkan error saat pertama kali dijalankan
        self.link = Database(
            self.config.get('database', 'engine'),
            host=self.config.get('database', 'host'),
            port=self.config.getint('database', 'port'),
            user=self.config.get('database', 'user'),
            passwd=self.config.get('database', 'password'),
            db=self.config.get('database', 'db'))

    def getLink(self):
        return self.link

    def generate(self):
        sql_debug(self.config.get('database', 'verbose'))
        self.link.generate_mapping(
            create_tables=self.config.get('database', 'create_table'))
