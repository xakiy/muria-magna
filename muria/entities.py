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
"""muria entities class."""

import uuid
from datetime import datetime, date
# from muria.config import conf
from settings import connection
from pony.orm import (PrimaryKey, Required, Optional, Set,
                      composite_key)  # composite_index)

link = connection.getLink()


def jinshi(s):
    return (('L', 'P').count(s))


'''
class Group(link.Entity):
    group = Required(str)
    person = set("Person")
    santri = set("Santri")
    pegawai = set("Pegawai")
    pengurus = set("Pengurus_Pesantren")
'''


class Person(link.Entity):
    id = PrimaryKey(str, 36, default=uuid.uuid4)
    nik = Required(str, 16, unique=True)  # no induk kependudukan
    nama = Required(str)
    tempat_lahir = Required(str)
    tanggal_lahir = Required(date)
    jenis_kelamin = Required(str, 2, py_check=jinshi)
    anak_ke = Optional(
        str, nullable=True)  # dalam format anak_ke/jumlah_saudara, misal 1/5
    tinggal_bersama = Optional(str, nullable=True)
    pekerjaan = Optional(str, nullable=True)
    penghasilan = Optional(int, nullable=True)
    pendidikan_terakhir = Optional(str, nullable=True)
    phone1 = Optional(str, nullable=True)
    phone2 = Optional(str, nullable=True)
    tanggal_update = Optional(datetime)
    tanggal_entry = Optional(datetime, index=True)
    harim = Set("Keluarga", reverse="mahram")
    mahram = Set("Keluarga", reverse="harim")
    pelajar = Optional("Pelajar_Lembaga", reverse="id", lazy=True)
    pegawai = Optional("Pegawai_Lembaga", reverse="id", lazy=True)
    pengguna = Optional("User", reverse="pid", lazy=True)
    alamat = Set("Alamat")


class Santri(Person):
    nis = Required(str, 20, unique=True)
    wali = Optional("Santri", reverse="asuhan")
    asuhan = Set("Santri", reverse="wali")
    tanggal_mulai = Optional(date)
    tanggal_akhir = Optional(date)
    pengurus = Optional("Pengurus_Pesantren", reverse="id", lazy=True)
    kepala_wilayah = Optional(
        "Asrama_Wilayah", reverse="kepala_wilayah", lazy=True)
    kepala_blok = Optional("Asrama_Blok", reverse="kepala_blok", lazy=True)
    kepala_kamar = Optional("Asrama_Kamar", reverse="ketua_kamar", lazy=True)
    menghuni_kamar = Optional(
        "Asrama_Kamar", reverse="penghuni_kamar", lazy=True)


class Keluarga(link.Entity):
    harim = Required("Person", reverse="mahram")
    mahram = Required("Person", reverse="harim")
    relasi = Required("Hubungan_Keluarga", reverse="hubungan")


class Hubungan_Keluarga(link.Entity):
    hubungan = Set("Keluarga", reverse="relasi")
    nama_relasi = Required(str)
    nama_relasi_terbalik = Required(str)
    jenis_kelamin = Required(str, 2)


class Asrama_Wilayah(link.Entity):
    id = PrimaryKey(int, auto=True)
    nama_wilayah = Required(str, unique=True)
    kepala_wilayah = Required("Santri", index=True, nullable=True)
    lokasi_wilayah = Optional(str, nullable=True)
    area_wilayah = Required(str, 2, py_check=jinshi)
    blok_wilayah = Set("Asrama_Blok")
    #composite_key("id", "kepala_wilayah")


class Asrama_Blok(link.Entity):
    id = PrimaryKey(int, auto=True)
    nama_blok = Required(str)
    kepala_blok = Required("Santri", index=True, nullable=True)
    wilayah = Required("Asrama_Wilayah")
    kamar = Set("Asrama_Kamar")
    # composite_key("id", "kepala_blok")


class Asrama_Kamar(link.Entity):
    id = PrimaryKey(int, auto=True)
    nama_kamar = Required(
        str, 30)  # tidak perlu unique, karena nama_kamar, blok composite key
    ketua_kamar = Required("Santri", index=True)
    blok = Required("Asrama_Blok")
    jumlah_penghuni = Optional(int, default=1)
    penghuni_kamar = Set("Santri", reverse="menghuni_kamar")
    composite_key("nama_kamar", "blok")


class Lembaga(link.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    slug = Required(str, 20, unique=True)
    nama = Required(str, unique=True)
    nama_panjang = Optional(str)
    lokasi = Optional(str, nullable=True)
    keterangan = Optional(str, nullable=True)
    pelajar = Set("Pelajar_Lembaga")
    pegawai = Set("Pegawai_Lembaga")
    jabatan = Set("Jabatan_Lembaga")


class Pangkat_Jabatan(link.Entity):
    kode = PrimaryKey(str, 10)
    nama_pangkat = Optional(str, 45, nullable=True)
    golongan = Optional(str, 5)
    ruang = Optional(str, 5)
    eselon = Set("Pegawai_Lembaga")


class Jabatan_Lembaga(link.Entity):  # Immutable, bisa diupdate sesuai kebutuhan
    id = PrimaryKey(int, size=8, auto=True)
    jabatan = Required(str)
    lembaga = Required("Lembaga")
    keterangan = Optional(str, nullable=True)
    pejabat = Set("Pegawai_Lembaga", reverse="jabatan")
    composite_key("jabatan", "lembaga")


class Pelajar_Lembaga(link.Entity):
    id = PrimaryKey("Person", reverse="pelajar")
    no_induk = Required(str, 20, unique=True)  # No Induk Pelajar
    lembaga = Required("Lembaga")
    catatan = Optional(str)
    tanggal_mulai = Optional(date)
    tanggal_akhir = Optional(date)


class Pegawai_Lembaga(link.Entity):
    id = PrimaryKey("Person", reverse="pegawai")
    nip = Required(str, 30)  # No Induk Pegawai, buat baru bila bukan PNS
    lembaga = Required("Lembaga")
    jabatan = Required("Jabatan_Lembaga", reverse="pejabat")
    pangkat = Required("Pangkat_Jabatan")
    catatan = Optional(str, nullable=True)
    tanggal_mulai = Optional(date, nullable=True)
    tanggal_akhir = Optional(date, nullable=True)


class Biro_Kepesantrenan(link.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    nama = Required(str, unique=True)
    lokasi = Optional(str)
    keterangan = Optional(str)
    pengurus = Set("Pengurus_Pesantren")
    jabatan = Set("Jabatan_Biro_Kepesantrenan")


class Jabatan_Biro_Kepesantrenan(link.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    jabatan = Required(str)
    keterangan = Optional(str)
    biro = Required("Biro_Kepesantrenan", reverse="jabatan")
    pengurus = Set("Pengurus_Pesantren")


class Pengurus_Pesantren(link.Entity):
    id = PrimaryKey("Santri", reverse="pengurus")
    nip = Required(str, 20)  # No. Induk Pengurus
    biro = Required("Biro_Kepesantrenan")
    jabatan = Required("Jabatan_Biro_Kepesantrenan")
    catatan = Optional(str)
    tanggal_mulai = Optional(date)
    tanggal_akhir = Optional(date)


class Jenis_Alamat(link.Entity):
    jenis = Required(str)
    keterangan = Optional(str)
    alamat = Set("Alamat")


class Alamat(link.Entity):
    pemilik = Required("Person", reverse="alamat")
    jenis = Required("Jenis_Alamat")
    alamat = Required(str)
    kecamatan = Optional("Alamat_Kecamatan")
    kabupaten = Required("Alamat_Kabupaten")
    provinsi = Required("Alamat_Provinsi")
    negara = Required("Alamat_Negara")
    kodepos = Optional(str, 6)


class Alamat_Kecamatan(link.Entity):
    kode_kecamatan = Required(str, 15)
    nama_kecamatan = Required(str)
    kabupaten = Required("Alamat_Kabupaten", reverse="daftar_kecamatan")
    alamat = Set("Alamat")


class Alamat_Kabupaten(link.Entity):
    kode_kabupaten = Required(str, 9)
    nama_kabupaten = Required(str)
    provinsi = Required("Alamat_Provinsi", reverse="daftar_kabupaten")
    daftar_kecamatan = Set("Alamat_Kecamatan", reverse="kabupaten")
    alamat = Set("Alamat")


class Alamat_Provinsi(link.Entity):
    kode_provinsi = Required(str, 5)
    nama_provinsi = Required(str)
    negara = Required("Alamat_Negara", reverse="daftar_provinsi")
    daftar_kabupaten = Set("Alamat_Kabupaten", reverse="provinsi")
    alamat = Set("Alamat")


class Alamat_Negara(link.Entity):
    nama_negara = Required(str)
    kode_iso = Required(str, 2)
    daftar_provinsi = Set("Alamat_Provinsi", reverse="negara")
    alamat = Set("Alamat")


class User(link.Entity):
    pid = PrimaryKey("Person", reverse="pengguna")
    """ Person.id in UUID form """
    username = Required(str, 40)
    password = Required(str)
    email = Required(str)
    group = Set("Group")
    # token = Required(str)
    # token_validity = Required(date)
    # client = Optional(str)


class Group(link.Entity):
    name = Required(str)
    note = Optional(str)
    member = Set("User")


'''
class alumni(link.Entity):
class jejak_rekam(link.Entity):
class khadam(link.Entity):
'''

connection.generate()
