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
"""muria schema class."""

from marshmallow import (
    Schema,
    fields,
    pre_dump,
    post_load,
    validates_schema,
    ValidationError,
    validates)
from marshmallow.validate import (Length, Regexp)
from muria.db.model import *
from muria.lib.misc import json, isJinshi
from htmllaundry import strip_markup
from uuid import UUID
import re
import datetime


class Skema(Schema):
    class Meta:
        json_module = json


class UID(fields.UUID):
    """A UUID field."""

    def _serialize(self, value, attr, obj):
        validated = str(self._validated(value)) if value is not None else None
        return str(validated)


class Tanggal(fields.Date):
    """Bare ISO8601-formatted date string without time. """

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return value.isoformat()[:10]
        except AttributeError:
            self.fail('format', input=value)
        return value


class Orang_Schema(Skema):
    id = UID(required=True, default=uuid.uuid4)
    nik = fields.String(required=True, validate=Length(min=16, max=16, error='NIK harus 16 digit'))
    nama = fields.String(required=True)
    jinshi = fields.String(required=True, validate=isJinshi)
    tempat_lahir = fields.String(required=True)
    tanggal_lahir = Tanggal(required=True)
    telepon = fields.Nested("Telepon_Schema", only=('id', 'jenis'), many=True)
    pendidikan_akhir = fields.Nested(
        "Pendidikan_Akhir_Schema",
        only=('nama', 'singkatan'), allow_none=True)
    alamat = fields.Nested(
        "Alamat_Schema",
        only=('jenis', 'alamat', 'default'), many=True)
    pekerjaan = fields.Nested("Pekerjaan_Schema", only=('nama'))
    tanggal_masuk = Tanggal(dump_only=True)


class Santri_Schema(Orang_Schema):
    # 2004-12-51-16-41-9999
    # aaaa bb cc dd ee ffff
    # aaaa = tahun kelahiran
    # bb   = bulan kelahiran
    # cc   = tanggal kelahiran tambah 50 bila perempuan
    # dd   = tahun masuk pesantren
    # ee   = e[pertama: nomor jenjang pendidikan]
    #        e[kedua: tahun angkatan]
    #        4 = TMI, 1 = kelas 1
    #        4 = TMI, 2 = intensif
    #        4 = TMI, 4 = intensif kelas 4
    #        5 = Strata 1, 2 = tahun ke 2
    # ffff = nomor urut pendaftaran
    nis = fields.String(required=True, validate=Length(min=16, max=16, error='NIS tidak tepat'))
    anak_ke = fields.Integer(allow_none=True)
    jumlah_saudara = fields.Integer(allow_none=True)
    tinggal_bersama = fields.String(allow_none=True)
    penanggung_biaya = fields.String(required=True, default='ayah')
    domisili = fields.Nested(
        "Penghuni_Kamar_Schema",
        only=('asrama_kamar', 'tanggal_masuk', 'tanggal_keluar'),
        many=True)
    orang_tua = fields.Nested("Relasi_Schema", only=('ortu', 'figur'), many=True)
    hobi = fields.Nested("Hobi_Santri_Schema", only='hobi', many=True)


class Ortu_Schema(Orang_Schema):
    pendapatan = fields.Integer(allow_none=True)
    anak = fields.Nested("Relasi_Schema", only=('santri', 'figur'), many=True)


class Alumni_Schema(Santri_Schema):
    tanggal_lulus = Tanggal(allow_none=True)
    ijazah_akhir = fields.Nested("Pendidikan_Akhir_Schema", only='jenjang')


class Data_Alamat(Skema):
    id = fields.Integer(required=True)
    jalan = fields.String(required=True, allow_none=True)
    kode_pos = fields.String(allow_none=True)
    kelurahan = fields.Nested('Alamat_Kelurahan_Schema')
    kecamatan = fields.Nested('Alamat_Kecamatan_Schema')
    kabupaten = fields.Nested('Alamat_Kabupaten_Schema')
    provinsi = fields.Nested('Alamat_Provinsi_Schema')
    negara = fields.Nested('Alamat_Negara_Schema')


class Alamat_Kelurahan_Schema(Skema):
    kode = fields.String(required=True)
    nama = fields.String(required=True)
    kecamatan = fields.Nested('Alamat_Kecamatan_Schema')
    data_alamat = fields.Nested('Data_Alamat_Schema')


class Alamat_Kecamatan_Schema(Skema):
    kode = fields.String(required=True)
    nama = fields.String(required=True)
    kelurahan = fields.Nested('Alamat_Kelurahan_Schema')
    kabupaten = fields.Nested('Alamat_Kabupaten_Schema')
    data_alamat = fields.Nested('Data_Alamat_Schema')


class Alamat_Kabupaten_Schema(Skema):
    kode = fields.String(required=True)
    nama = fields.String(required=True)
    kecamatan = fields.Nested('Alamat_Kecamatan_Schema')
    provinsi = fields.Nested('Alamat_Provinsi_Schema')
    data_alamat = fields.Nested('Data_Alamat_Schema')


class Alamat_Provinsi_Schema(Skema):
    kode = fields.String(required=True)
    nama = fields.String(required=True)
    kabupaten = fields.Nested('Alamat_Kabupaten_Schema')
    negara = fields.Nested('Alamat_Negara_Schema')
    data_alamat = fields.Nested('Data_Alamat_Schema')


class Alamat_Negara_Schema(Skema):
    iso = fields.String(required=True)
    iso3 = fields.String(allow_none=True, missing=None)
    nomor = fields.Integer(allow_none=True, missing=None)
    kode_telp = fields.String(allow_none=True, missing=None)
    nama = fields.String(required=True)
    provinsis = fields.Nested('Alamat_Provinsi_Schema')
    data_alamat = fields.Nested('Data_Alamat_Schema')


class Jenis_Alamat_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)


class Hobi_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(allow_none=True, missing=None)
    hobi_santri = fields.Nested('Hobi_Santri_Schema')
    kategori = fields.Nested('Kategori_Hobi_Schema')


class Kategori_Hobi_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(allow_none=True, missing=None)
    hobi = fields.Nested('Hobi_Schema')


class Jenis_Telepon_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    telepon = fields.Nested('Telepon')


class Asrama_Rayon_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    kamar = fields.Nested('Asrama_Kamar_Schema', required=False)
    area = fields.Nested('Jinshi_Schema', only='kecil')
    jenis = fields.Nested('Jenis_Asrama_Schema', only='nama')


class Asrama_Kamar_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    penghuni_kamar = fields.Nested('Penghuni_Kamar')
    rayon = fields.Nested('Asrama_Rayon_Schema')


class Jenis_Asrama_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    asrama = fields.Nested('Asrama_Rayon_Schema')


class Penghuni_Kamar_Schema(Skema):
    aktif = Required(bool, default=True)
    santri = fields.Nested('Santri_Schema')
    asrama_kamar = fields.Nested('Asrama_Kamar_Schema')
    tanggal_masuk = Tanggal()
    tanggal_keluar = Tanggal()


class Pendidikan_Akhir_Schema(Skema):
    id = fields.Integer(required=True)
    jenjang = fields.Nested('Tingkat_Pendidikan_Schema')
    sekolah = fields.String(allow_none=True, missing=None)
    tahun = Required(date, unique=True)
    no_ijazah = Optional(str, unique=True, nullable=True)
    orang = fields.Nested('Orang_Schema')
    alumni = fields.Nested('Alumni_Schema')


class Tingkat_Pendidikan_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    singkatan = fields.String(required=True)
    pendidikan_akhir = fields.Nested('Pendidikan_Akhir_Schema')


class Pekerjaan_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(allow_none=True, missing=None)
    orang = fields.Nested('Orang_Schema')


class Jinshi_Schema(Skema):
    id = fields.String(required=True)
    nama = fields.String()
    kecil = fields.String(allow_none=True, missing=None)
    formal = fields.String(allow_none=True, missing=None)


class Pengguna_Schema(Skema):
    orang = fields.Nested('Orang_Schema', only=('id', 'nama', 'jinshi', 'tempat_lahir', 'tanggal_lahir', 'tanggal_masuk'), dump_to='profile')
    username = fields.String(required=True, validate=Regexp(r'^[a-z]+(?:[_.]?[a-zA-Z0-9]){7,28}$', re.U & re.I))
    email = fields.Email(missing=None, allow_none=True)
    kewenangan = fields.Nested('Kewenangan_Schema', only=('wewenang'), dump_to='wewenang')
    password = fields.String(validate=Length(min=64, max=64), load_only=True)
    suspended = fields.Boolean(required=True, missing=False)


class Login_Schema(Skema):
    username = fields.String(required=True, validate=Regexp(r'^[a-z]+(?:[_.]?[a-zA-Z0-9]){7,28}$', re.U & re.I))
    password = fields.String(required=True, validate=Length(min=64, max=64))


class Grup_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(required=True)
    keterangan = fields.String(allow_none=True, missing=None)
    wewenang = fields.Nested('Grup_Wewenang')


class Figur_Ortu_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(allow_none=True, missing=None)
    relasi = fields.Nested('Relasi_Schema')


class Relasi_Schema(Skema):
    ortu = fields.Nested('Ortu_Schema')
    santri = fields.Nested('Santri_Schema')
    figur = fields.Nested('Figur_Ortu_Schema')


class Telepon_Schema(Skema):
    id = fields.Integer(required=True)
    nomor = fields.String()
    orang = fields.Nested('Orang_Schema')
    jenis = fields.Nested('Jenis_Telepon_Schema')
    kode_negara = fields.String(default="62")
    kode_regional = fields.String(allow_none=True, missing=None)


class Alamat_Schema(Skema):
    default = fields.Boolean(default=False)
    orang = fields.Nested('Orang_Schema')
    jenis = fields.Nested('Jenis_Alamat_Schema')
    alamat = fields.Nested('Data_Alamat_Schema')


class Hobi_Santri_Schema(Skema):
    santri = fields.Nested('Santri_Schema', only=('id', 'nama'))
    hobi = fields.Nested('Hobi_Schema', only=('id', 'nama'))


class Wewenang_Schema(Skema):
    id = fields.Integer(required=True)
    nama = fields.String(allow_none=True, missing=None)
    pengguna = fields.Nested('Pengguna_Schema')
    grup = fields.Nested('Grup_Wewenang_Schema')


class Grup_Wewenang_Schema(Skema):
    grup = fields.Nested('Grup_Schema')
    wewenang = fields.Nested('Wewenang_Schema')


class Online_Schema(Skema):
    id = fields.Integer(required=True)
    rkey = fields.String(required=True)
    akey = fields.String()
    uakey = fields.String(required=True)
    pengguna = fields.Nested('Pengguna_Schema')
    referrer = fields.String(missing=None)
    ua = fields.String(required=True)
    loc = fields.String(missing=None)
    origin = fields.String(allow_none=False, missing=None)
    time = fields.DateTime(default=lambda: datetime.now())
    last_time = fields.String(allow_none=True, missing=None)
    rkey_period = fields.Integer(allow_none=True, missing=None)
    akey_period = fields.Integer(allow_none=True, missing=None)


class Offline_Schema(Skema):
    """online blacklist"""
    id = fields.Integer(required=True)
    online = fields.Nested('Online_Schema')
    rkey = fields.String(allow_none=True, missing=None)
    akey = fields.String(allow_none=True, missing=None)
    uakey = fields.String(allow_none=True, missing=None)


class Kewenangan_Schema(Skema):
    pengguna = fields.Nested('Pengguna_Schema')
    wewenang = fields.Nested('Wewenang_Schema', only=('id', 'nama'), many=True)
