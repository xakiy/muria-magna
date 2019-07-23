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
"""Some preloads of database content."""

tables = list()

jinshies = list()
jinshies.append({"id": "l", "nama": "Laki-laki", "kecil": "Putra", "formal": "Pria"})
jinshies.append({"id": "p", "nama": "Perempuan", "kecil": "Putri", "formal": "Wanita"})

tables.append({'model': 'Jinshi', 'data': jinshies})

figures = list()
figures.append({"nama_atas": "Ayah", "nama_bawah": "Anak"})
figures.append({"nama_atas": "Ibu", "nama_bawah": "Anak"})
figures.append({"nama_atas": "Wali", "nama_bawah": "Anak Asuh"})
tables.append({'model': 'Figur', 'data': figures})

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

wewenang = list()
wewenang.append({"id": 1, "nama": "root"})
wewenang.append({"id": 2, "nama": "admin"})
wewenang.append({"id": 3, "nama": "editor"})
wewenang.append({"id": 4, "nama": "kontributor"})
wewenang.append({"id": 5, "nama": "santriwan"})
wewenang.append({"id": 6, "nama": "santriwati"})
wewenang.append({"id": 7, "nama": "wali"})
wewenang.append({"id": 8, "nama": "umum"})
tables.append({'model': 'Wewenang', 'data': wewenang})
