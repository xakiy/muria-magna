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
from pony.orm.dbapiprovider import OperationalError


class DBManager(object):
    def __init__(self, config):
        self.config = config
        self.params = dict()
        self.params.update({"provider": self.config.get("database", "engine")})
        # MySQL and PostgreSQL
        if self.params["provider"] in ("mysql", "postgres"):
            self.params.update(
                {
                    "host": self.config.get("database", "host"),
                    "user": self.config.get("database", "user"),
                    "db": self.config.get("database", "db"),
                }
            )
            # mysql uses 'passwd' keyword argument instead of 'password'
            if self.params["provider"] == "mysql":
                self.params.update({"passwd": self.config.get("database", "password")})
            else:
                self.params.update(
                    {"password": self.config.get("database", "password")}
                )
            # use socket if available prior to TCP connection
            if self.config.get("database", "socket"):
                self.params.update(
                    {"unix_socket": self.config.get("database", "socket")}
                )
            port = self.config.get("database", "port")
            if port is not None and port.isnumeric():
                self.params.update({"port": int(port)})
        # SQLite
        elif self.params["provider"] == "sqlite":
            self.params.update({"filename": self.config.get("database", "filename")})
            if self.params["filename"] != ":memory:":
                self.params.update(
                    {"create_db": self.config.getboolean("database", "create_db")}
                )
        # Oracle
        elif self.params["provider"] == "oracle":
            self.params.update(
                {
                    "user": self.config.get("database", "user"),
                    "password": self.config.get("database", "password"),
                    "dsn": self.config.get("database", "dsn"),
                }
            )

        self._connect()

    def _connect(self):
        options = self.params
        if options["provider"] in ("mysql", "postgres"):
            if options.get("unix_socket") is not None:
                # try to connect using socket
                try:
                    if options.get("port"):
                        options.pop("port")
                    self.link = Database(**options)
                # else using TCP port
                except OperationalError as oe:
                    self.params.pop("unix_socket")
                    self.link = Database(**self.params)
        else:
            self.link = Database(**self.params)

    def getLink(self):
        return self.link

    def generate(self):
        sql_debug(self.config.getboolean("database", "verbose"))
        self.link.generate_mapping(
            create_tables=self.config.getboolean("database", "create_table")
        )
