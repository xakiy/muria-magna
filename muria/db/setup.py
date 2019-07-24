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

"""Database setup."""

import sys
from pony.orm import (
    Database as _Database,
    db_session,
    flush,
    sql_debug
)
from pony.orm.dbapiprovider import OperationalError
from muria.db.model import (
    connection,
    Orang,
    Santri,
    Ortu,
    Alumni,
    Data_Alamat,
    Alamat_Kelurahan,
    Alamat_Kecamatan,
    Alamat_Kabupaten,
    Alamat_Provinsi,
    Alamat_Negara,
    Jenis_Alamat,
    Hobi,
    Kategori_Hobi,
    Jenis_Telepon,
    Asrama_Rayon,
    Asrama_Kamar,
    Jenis_Asrama,
    Penghuni_Kamar,
    Pendidikan_Akhir,
    Tingkat_Pendidikan,
    Pekerjaan,
    Jinshi,
    Pengguna,
    Grup,
    Figur,
    Relasi,
    Telepon,
    Alamat,
    Hobi_Santri,
    Wewenang,
    Grup_Wewenang,
    Online,
    Offline,
    Kewenangan,
)
from muria.db.preload import tables

def setup_database(config):

    params = dict()
    params.update({"provider": config.get("database", "engine")})
    # MySQL and PostgreSQL
    if params["provider"] in ("mysql", "postgres"):
        params.update(
            {
                "host": config.get("database", "host"),
                "user": config.get("database", "user"),
                "db": config.get("database", "db"),
            }
        )
        # mysql uses 'passwd' keyword argument instead of 'password'
        if params["provider"] == "mysql":
            params.update({"passwd": config.get("database", "password")})
        else:
            params.update(
                {"password": config.get("database", "password")}
            )
        # use socket if available prior to TCP connection
        if config.get("database", "socket"):
            params.update(
                {"unix_socket": config.get("database", "socket")}
            )
        port = config.get("database", "port")
        if port is not None and port.isnumeric():
            params.update({"port": int(port)})
    # SQLite
    elif params["provider"] == "sqlite":
        params.update({"filename": config.get("database", "filename")})
        if params["filename"] != ":memory:":
            params.update(
                {"create_db": config.getboolean("database", "create_db")}
            )
    # Oracle
    elif params["provider"] == "oracle":
        params.update(
            {
                "user": config.get("database", "user"),
                "password": config.get("database", "password"),
                "dsn": config.get("database", "dsn"),
            }
        )

    if params["provider"] in ("mysql", "postgres"):
        options = params.copy()
        # if socket provided try to use it first
        if params.get("unix_socket") is not None:
            try:
                if params.get("port"):
                    params.pop("port")
                connection.bind(**params)
            # otherwise use TCP port
            except OperationalError as oe:
                options.pop("unix_socket")
                connection.bind(**options)
                params = options
    else:
        connection.bind(**params)

    # config.add_section('db')
    # config.read_dict({'db': params})

    sql_debug(config.getboolean("database", "verbose"))
    connection.generate_mapping(
        create_tables=config.getboolean("database", "create_table")
    )

    if tables is not []:
        with db_session:
            for table in tables:
                for row in table['data']:
                    model = getattr(sys.modules[__name__], table['model'])
                    if not model.exists(**row):
                        model(**row)
            flush()

