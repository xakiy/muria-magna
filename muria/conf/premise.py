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
"""Entity class."""

from datetime import datetime, date
from uuid import UUID
from pony.orm import db_session, flush
from muria.db.model import Jinshi, Figur, Wewenang

def makeJinshi():
    data = list()
    data.append({'id': 'l', 'nama': 'Laki-laki', 'kecil': 'Putra', 'formal': 'Pria'})
    data.append({'id': 'p', 'nama': 'Perempuan', 'kecil': 'Putri', 'formal': 'Wanita'})
    with db_session:
        for j in data:
            if not Jinshi.exists(**j):
                Jinshi(**j)
        flush()

def makeFigur():
    data = list()
    data.append({'nama_atas': 'Ayah', 'nama_bawah': 'Anak'})
    data.append({'nama_atas': 'Ibu', 'nama_bawah': 'Anak'})
    data.append({'nama_atas': 'Wali', 'nama_bawah': 'Anak Asuh'})

    with db_session:
        for f in data:
            if not Figur.exists(**f):
                Figur(**f)
        flush()

# CORS Policy
# def makeGrup():
    """
    +----+------------+------------+
    | id | nama       | keterangan |
    +----+------------+------------+
    |  1 | deleter    | NULL       |
    |  2 | editor     | NULL       |
    |  3 | creator    | NULL       |
    |  4 | reader     | NULL       |
    |  5 | pengurus   | NULL       |
    |  6 | pengajar   | NULL       |
    |  7 | tu         | NULL       |
    |  8 | santriwan  | NULL       |
    |  9 | santriwati | NULL       |
    | 10 | umum       | NULL       |
    +----+------------+------------+
    """

# CORS Policy combined with Wewenang
# def makeGrupWewenang():
    # pass

# def makeJenisAlamat():
    """
    +----+--------+
    | id | nama   |
    +----+--------+
    |  1 | Rumah  |
    |  2 | Kantor |
    |  3 | Surat  |
    +----+--------+
    """

# def makeJenisAsrama():
    """
    +----+---------------------+
    | id | nama                |
    +----+---------------------+
    |  1 | Asrama              |
    |  5 | Asrama Guru         |
    |  7 | Balai Latihan Kerja |
    |  6 | Gedung Kelas        |
    |  4 | Gudang              |
    |  8 | Kantin              |
    |  2 | Kantor              |
    |  3 | Rumah Guru          |
    |  9 | Unit Kesehatan      |
    +----+---------------------+
    """

# def makeJenisTelepon():
    # pass

# def makeTingkatPendidikan():
    """
    +----+--------------------------+-----------+
    | id | nama                     | singkatan |
    +----+--------------------------+-----------+
    |  1 | Sekolah Dasar            | SD        |
    |  2 | Sekolah Menengah Pertama | SMP       |
    |  3 | Sekolah Menengah Atas    | SMA       |
    |  4 | Sarjana Muda             | Diploma   |
    |  5 | Sarjana                  | S1        |
    |  6 | Magister/Master          | S2        |
    |  7 | Doktor                   | S3        |
    +----+--------------------------+-----------+
    """

def makeWewenang():
    data = list()
    data.append({'id': 1, 'nama': 'root'})
    data.append({'id': 2, 'nama': 'admin'})
    data.append({'id': 3, 'nama': 'editor'})
    data.append({'id': 4, 'nama': 'kontributor'})
    data.append({'id': 5, 'nama': 'santriwan'})
    data.append({'id': 6, 'nama': 'santriwati'})
    data.append({'id': 7, 'nama': 'wali'})
    data.append({'id': 8, 'nama': 'umum'})

    with db_session:
        for w in data:
            if not Wewenang.exists(**w):
                Wewenang(**w)
        flush()

def setPremise():
    makeJinshi()
    makeFigur()
    makeWewenang()
