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
from init import connection
from db.mixin import *
from pony.orm import (PrimaryKey, Required, Optional, Set,
                      composite_key)  # composite_index)

db = link = connection.getLink()


class Orang(db.Entity, Mixin_Loader):
    id = PrimaryKey(UUID)
    nik = Required(int, size=64, unique=True)
    nama = Required(str, 60)
    jinshi = Required('Jinshi')
    tempat_lahir = Required(str, 60)
    tanggal_lahir = Required(date)
    telepon = Set('Telepon')
    pendidikan_akhir = Optional('Pendidikan_Akhir')
    alamat = Set('Alamat')
    pekerjaan = Optional('Pekerjaan')
    tanggal_masuk = Optional(date, default=lambda: date.today())
    pengguna = Optional('Pengguna')


class Santri(Orang, Mixin_Loader):
    nis = Optional(int, size=64, unique=True)
    anak_ke = Optional(int, size=8)
    jumlah_saudara = Optional(int, size=8)
    tinggal_bersama = Optional(str, 60)
    penanggung_biaya = Required(str, default='ayah')
    domisili = Set('Penghuni_Kamar')
    orang_tua = Set('Relasi')
    hobi = Set('Hobi_Santri')


class Ortu(Orang, Mixin_Loader):
    pendapatan = Optional(int)
    anak = Set('Relasi')


class Alumni(Santri, Mixin_Loader):
    tanggal_lulus = Optional(date)
    ijazah_akhir = Optional('Pendidikan_Akhir')


class Data_Alamat(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    jalan = Required(str, nullable=True)
    kode_pos = Optional(str, 5, nullable=True)
    kelurahan = Required('Alamat_Kelurahan')
    kecamatan = Required('Alamat_Kecamatan')
    kabupaten = Required('Alamat_Kabupaten')
    provinsi = Required('Alamat_Provinsi')
    negara = Required('Alamat_Negara')
    daftar_alamat = Set('Alamat')


class Alamat_Kelurahan(db.Entity, Mixin_Loader):
    kode = PrimaryKey(str, 10)
    nama = Required(str)
    kecamatan = Required('Alamat_Kecamatan')
    data_alamat = Set(Data_Alamat)


class Alamat_Kecamatan(db.Entity, Mixin_Loader):
    kode = PrimaryKey(str, 7)
    nama = Required(str)
    kelurahan = Set(Alamat_Kelurahan)
    kabupaten = Required('Alamat_Kabupaten')
    data_alamat = Set(Data_Alamat)


class Alamat_Kabupaten(db.Entity, Mixin_Loader):
    kode = PrimaryKey(str, 4)
    nama = Required(str)
    kecamatan = Set(Alamat_Kecamatan)
    provinsi = Required('Alamat_Provinsi')
    data_alamat = Set(Data_Alamat)


class Alamat_Provinsi(db.Entity, Mixin_Loader):
    kode = PrimaryKey(str, 2)
    nama = Required(str)
    kabupaten = Set(Alamat_Kabupaten)
    negara = Required('Alamat_Negara')
    data_alamat = Set(Data_Alamat)


class Alamat_Negara(db.Entity, Mixin_Loader):
    iso = PrimaryKey(str, 2)
    iso3 = Optional(str, 3, unique=True)
    nomor = Optional(int, size=16, unique=True)
    kode_telp = Optional(str, 4)
    nama = Required(str)
    provinsi = Set(Alamat_Provinsi)
    data_alamat = Set(Data_Alamat)


class Jenis_Alamat(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Required(str)
    alamat = Set('Alamat')


class Hobi(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Optional(str, unique=True)
    hobi_santri = Set('Hobi_Santri')
    kategori = Required('Kategori_Hobi')


class Kategori_Hobi(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Optional(str)
    hobi = Set(Hobi)


class Jenis_Telepon(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Required(str, 20, unique=True)
    telepon = Set('Telepon')


class Asrama_Rayon(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 40, unique=True)
    kamar = Set('Asrama_Kamar')
    area = Required('Jinshi')
    jenis = Required('Jenis_Asrama')


class Asrama_Kamar(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 40, unique=True)
    penghuni_kamar = Set('Penghuni_Kamar')
    rayon = Required(Asrama_Rayon)


class Jenis_Asrama(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 20, unique=True)
    asrama = Set(Asrama_Rayon)


class Penghuni_Kamar(db.Entity, Mixin_Loader):
    aktif = Required(bool, default=True)
    santri = Required(Santri)
    asrama_kamar = Required(Asrama_Kamar)
    tanggal_masuk = Optional(date)
    tanggal_keluar = Optional(date)
    PrimaryKey(santri, asrama_kamar)


class Pendidikan_Akhir(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    jenjang = Required('Tingkat_Pendidikan')
    sekolah = Optional(str, nullable=True)
    tahun = Required(date, unique=True)
    no_ijazah = Optional(str, unique=True, nullable=True)
    orang = Set(Orang)
    alumni = Set(Alumni)


class Tingkat_Pendidikan(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    singkatan = Required(str)
    pendidikan_akhir = Set(Pendidikan_Akhir)


class Pekerjaan(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Optional(str, 60)
    orang = Set(Orang)


class Jinshi(db.Entity, Mixin_Loader):
    id = PrimaryKey(str, 1)
    nama = Optional(str, 20, unique=True)
    kecil = Optional(str, 20)
    formal = Optional(str, 20)
    orang = Set(Orang)
    rayon = Set(Asrama_Rayon)


class Pengguna(db.Entity, Mixin_Loader):
    orang = PrimaryKey(Orang)
    username = Required(str, 40, unique=True)
    email = Required(str, 60, unique=True)
    password = Required(str)
    suspended = Required(bool, default=False)
    wewenang = Required('Wewenang')
    koneksi = Set('Online')


class Grup(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 30, unique=True)
    keterangan = Optional(str, nullable=True)
    wewenang = Set('Grup_Wewenang')


class Figur(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, size=8, auto=True)
    nama_atas = Required(str, unique=True)
    nama_bawah = Required(str)
    relasi = Set('Relasi')


class Relasi(db.Entity, Mixin_Loader):
    ortu = Required(Ortu)
    santri = Required(Santri)
    figur = Required(Figur)
    PrimaryKey(ortu, santri)


class Telepon(db.Entity, Mixin_Loader):
    id = PrimaryKey(int, auto=True)
    nomor = Required(str, 20)
    orang = Required(Orang)
    jenis = Required(Jenis_Telepon)
    kode_negara = Optional(str, 4, default="62")
    kode_regional = Optional(str, 4)


class Alamat(db.Entity, Mixin_Loader):
    default = Optional(bool, default=False)
    orang = Required(Orang)
    jenis = Required(Jenis_Alamat)
    alamat = Required(Data_Alamat)
    PrimaryKey(orang, alamat)


class Hobi_Santri(db.Entity, Mixin_Loader):
    santri = Required(Santri)
    hobi = Required(Hobi)
    PrimaryKey(santri, hobi)


class Wewenang(db.Entity, Mixin_Loader):
    """roles of users"""
    id = PrimaryKey(int, auto=True)
    nama = Optional(str)
    pengguna = Set(Pengguna)
    grup = Set('Grup_Wewenang')


class Grup_Wewenang(db.Entity, Mixin_Loader):
    grup = Required(Grup)
    wewenang = Required(Wewenang)
    PrimaryKey(grup, wewenang)


class Online(db.Entity, Mixin_Loader):
    # id = Required(int, size=64, unsigned=True)
    id = Required(int, size=64)
    rkey = Required(str, unique=True)
    akey = Required(str, unique=True)
    uakey = Required(str)
    pengguna = Required(Pengguna)
    referrer = Optional(str)
    ua = Optional(str)
    loc = Optional(str)
    origin = Optional(str)
    time = Required(datetime, default=lambda: datetime.now())
    last_time = Optional(str)
    rkey_period = Optional(int)
    akey_period = Optional(int)
    offline = Optional('Offline')
    PrimaryKey(id, uakey, pengguna)


class Offline(db.Entity, Mixin_Loader):
    """online blacklist"""
    # id = PrimaryKey(int, size=64, auto=True, unsigned=True)
    id = PrimaryKey(int, size=64, auto=True)
    online = Required(Online)
    rkey = Optional(str)
    akey = Optional(str)
    uakey = Optional(str)

connection.generate()
