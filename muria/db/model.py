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

import uuid
import hashlib
import binascii
from os import urandom
from datetime import datetime, date
from muria.init import connection
from pony.orm import (
    PrimaryKey,
    Required,
    Optional,
    Set,
    composite_index,
    composite_key,
    commit,
)

db = link = connection.getLink()


class Orang(db.Entity):
    id = PrimaryKey(str, 36, default=uuid.uuid4)
    nik = Required(int, size=64, unique=True)
    nama = Required(str, 60)
    jinshi = Required("Jinshi")
    tempat_lahir = Required(str, 60)
    tanggal_lahir = Required(date)
    telepon = Set("Telepon")
    pendidikan_akhir = Optional("Pendidikan_Akhir")
    alamat = Set("Alamat")
    pekerjaan = Optional("Pekerjaan")
    tanggal_masuk = Optional(date, default=lambda: date.today())
    pengguna = Optional("Pengguna", cascade_delete=True, lazy=True)


class Santri(Orang):
    nis = Optional(int, size=64, unique=True)
    anak_ke = Optional(int, size=8)
    jumlah_saudara = Optional(int, size=8)
    tinggal_bersama = Optional(str, 60)
    penanggung_biaya = Required(str, default="ayah")
    domisili = Set("Penghuni_Kamar", cascade_delete=True)
    orang_tua = Set("Relasi", cascade_delete=True)
    hobi = Set("Hobi_Santri", cascade_delete=True)


class Ortu(Orang):
    pendapatan = Optional(int)
    anak = Set("Relasi", cascade_delete=True)


class Alumni(Santri):
    tanggal_lulus = Optional(date)
    ijazah_akhir = Optional("Pendidikan_Akhir")


class Data_Alamat(db.Entity):
    id = PrimaryKey(int, auto=True)
    jalan = Required(str, 250, nullable=True)
    kode_pos = Optional(str, 5, nullable=True)
    kelurahan = Required("Alamat_Kelurahan")
    kecamatan = Required("Alamat_Kecamatan")
    kabupaten = Required("Alamat_Kabupaten")
    provinsi = Required("Alamat_Provinsi")
    negara = Required("Alamat_Negara")
    daftar_alamat = Set("Alamat")


class Alamat_Kelurahan(db.Entity):
    kode = PrimaryKey(str, 10)
    nama = Required(str, 200)
    kecamatan = Required("Alamat_Kecamatan")
    data_alamat = Set(Data_Alamat)


class Alamat_Kecamatan(db.Entity):
    kode = PrimaryKey(str, 7)
    nama = Required(str, 200)
    kelurahan = Set(Alamat_Kelurahan)
    kabupaten = Required("Alamat_Kabupaten")
    data_alamat = Set(Data_Alamat)


class Alamat_Kabupaten(db.Entity):
    kode = PrimaryKey(str, 4)
    nama = Required(str, 200)
    kecamatan = Set(Alamat_Kecamatan)
    provinsi = Required("Alamat_Provinsi")
    data_alamat = Set(Data_Alamat)


class Alamat_Provinsi(db.Entity):
    kode = PrimaryKey(str, 2)
    nama = Required(str, 200)
    kabupaten = Set(Alamat_Kabupaten)
    negara = Required("Alamat_Negara")
    data_alamat = Set(Data_Alamat)


class Alamat_Negara(db.Entity):
    iso = PrimaryKey(str, 2)
    iso3 = Optional(str, 3, unique=True)
    nomor = Optional(int, size=16, unique=True)
    kode_telp = Optional(str, 4)
    nama = Required(str, 200)
    provinsi = Set(Alamat_Provinsi)
    data_alamat = Set(Data_Alamat)


class Jenis_Alamat(db.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Required(str, 60)
    alamat = Set("Alamat")


class Hobi(db.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Optional(str, 50, unique=True)
    hobi_santri = Set("Hobi_Santri", cascade_delete=True)
    kategori = Required("Kategori_Hobi")


class Kategori_Hobi(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Optional(str, 50)
    hobi = Set(Hobi)


class Jenis_Telepon(db.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Required(str, 20, unique=True)
    telepon = Set("Telepon")


class Asrama_Rayon(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 40, unique=True)
    kamar = Set("Asrama_Kamar")
    area = Required("Jinshi")
    jenis = Required("Jenis_Asrama")


class Asrama_Kamar(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 40, unique=True)
    penghuni_kamar = Set("Penghuni_Kamar")
    rayon = Required(Asrama_Rayon)


class Jenis_Asrama(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 20, unique=True)
    asrama = Set(Asrama_Rayon)


class Penghuni_Kamar(db.Entity):
    aktif = Required(bool, default=True)
    santri = Required(Santri)
    asrama_kamar = Required(Asrama_Kamar)
    tanggal_masuk = Optional(date)
    tanggal_keluar = Optional(date)
    PrimaryKey(santri, asrama_kamar)


class Pendidikan_Akhir(db.Entity):
    id = PrimaryKey(int, auto=True)
    jenjang = Required("Tingkat_Pendidikan")
    sekolah = Optional(str, 200, nullable=True)
    tahun = Required(date, unique=True)
    no_ijazah = Optional(str, 150, unique=True, nullable=True)
    orang = Set(Orang)
    alumni = Set(Alumni)


class Tingkat_Pendidikan(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 200)
    singkatan = Required(str)
    pendidikan_akhir = Set(Pendidikan_Akhir)


class Pekerjaan(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Optional(str, 60)
    orang = Set(Orang)


class Jinshi(db.Entity):
    id = PrimaryKey(str, 1)
    nama = Optional(str, 20, unique=True)
    kecil = Optional(str, 20)
    formal = Optional(str, 20)
    orang = Set(Orang)
    rayon = Set(Asrama_Rayon)

    def __str__(self):
        return self.id


class Pengguna(db.Entity):
    orang = PrimaryKey(Orang)
    username = Required(str, 40, unique=True)
    email = Required(str, 60, unique=True)
    picture = Optional(str, 500, nullable=True)
    password = Required(str)
    salt = Required(str)
    suspended = Required(bool, default=False)
    kewenangan = Set("Kewenangan", cascade_delete=True)
    koneksi = Set("Online", cascade_delete=True)
    # alter table pengguna add `picture` varchar(500) NULL after email;
    # alter table pengguna add `salt` varchar(255) NOT NULL after password;

    def checkPassword(self, password_string):
        salt_bin = binascii.unhexlify(self.salt)
        password_digest = hashlib.sha256(bytes(password_string, "utf8")).digest()
        hashed_bin = hashlib.sha256(password_digest).digest()
        hashed_bin_key = hashlib.pbkdf2_hmac("sha256", hashed_bin, salt_bin, 1000)
        return hashed_bin_key.hex() == self.password


class Grup(db.Entity):
    """
    Grup mewakili dan menghimpun apa saja yang dimiliki
    oleh sebuah resource berdasarkan verba HTTP yang ada.
    """

    id = PrimaryKey(int, auto=True)
    nama = Required(str, 30, unique=True)
    keterangan = Optional(str, nullable=True)
    wewenang = Set("Grup_Wewenang")


class Figur(db.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    nama_atas = Required(str, 40, unique=True)
    nama_bawah = Required(str, 40)
    relasi = Set("Relasi")


class Relasi(db.Entity):
    ortu = Required(Ortu)
    santri = Required(Santri)
    figur = Required(Figur)
    PrimaryKey(ortu, santri)


class Telepon(db.Entity):
    id = PrimaryKey(int, auto=True)
    nomor = Required(str, 20)
    orang = Required(Orang)
    jenis = Required(Jenis_Telepon)
    kode_negara = Optional(str, 4, default="62")
    kode_regional = Optional(str, 4)


class Alamat(db.Entity):
    default = Optional(bool, default=False)
    orang = Required(Orang)
    jenis = Required(Jenis_Alamat)
    alamat = Required(Data_Alamat)
    PrimaryKey(orang, alamat)


class Hobi_Santri(db.Entity):
    santri = Required(Santri)
    hobi = Required(Hobi)
    PrimaryKey(santri, hobi)


class Wewenang(db.Entity):
    """roles of users"""

    id = PrimaryKey(int, auto=True)
    nama = Optional(str, 50)
    kewenangan = Set("Kewenangan")
    grup = Set("Grup_Wewenang")


class Grup_Wewenang(db.Entity):
    wewenang = Required(Wewenang)
    grup = Required(Grup)
    PrimaryKey(wewenang, grup)


class Online(db.Entity):
    id = PrimaryKey(int, size=64, auto=True)
    rkey = Required(str, sql_type="text")
    akey = Required(str, sql_type="text")
    uakey = Required(str, sql_type="text")
    pengguna = Required(Pengguna)
    referrer = Optional(str)
    ua = Optional(str)
    loc = Optional(str)
    origin = Optional(str)
    time = Required(datetime, default=lambda: datetime.now())
    last_time = Optional(str)
    rkey_period = Optional(int)
    akey_period = Optional(int)
    offline = Optional("Offline")


class Offline(db.Entity):
    """online blacklist"""

    id = PrimaryKey(int, size=64, auto=True)
    online = Required(Online)
    rkey = Optional(str)
    akey = Optional(str)
    uakey = Optional(str)


class Kewenangan(db.Entity):
    pengguna = Required(Pengguna)
    wewenang = Required(Wewenang)
    PrimaryKey(pengguna, wewenang)


connection.generate()
