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

""" DBManager class """

from pony.orm import Database, sql_debug

class DBManager(object):
    def __init__(self, config):
        self.config = config
        self.params = dict()
        self.params.update({'provider': self.config.get('database', 'engine')})
        # tanpa try-except untuk menampakkan error saat pertama kali dijalankan
        # MySQL and PostgreSQL
        if self.params['provider'] in ('mysql', 'postgres'):
            self.params.update({
                'host': self.config.get('database', 'host'),
                'user': self.config.get('database', 'user'),
                'passwd': self.config.get('database', 'password'),
                'db': self.config.get('database', 'db')
            })
            if self.config.get('database', 'socket'):
                self.params.update({
                    'unix_socket':
                    self.config.get('database', 'socket')
                })
            else:
                self.params.update({
                    'port':
                    self.config.getint('database', 'port')
                })
        # SQLite
        elif self.params['provider'] == 'sqlite':
            self.params.update({
                'filename': self.config.get('database', 'filename')
            })
            if self.params['filename'] != ':memory:':
                self.params.update({
                    'create_db':
                    self.config.getboolean('database', 'create_db')
                })
        # Oracle
        elif self.params['provider'] == 'oracle':
            self.params.update({
                'user': self.config.get('database', 'user'),
                'passwd': self.config.get('database', 'password'),
                'dsn': self.config.get('database', 'dsn')
            })

        self.link = Database(**self.params)

    def getLink(self):
        return self.link

    def generate(self):
        sql_debug(self.config.getboolean('database', 'verbose'))
        self.link.generate_mapping(
            create_tables=self.config.get('database', 'create_table'))
