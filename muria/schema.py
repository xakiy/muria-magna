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
    post_load,
    validates_schema,
    ValidationError)
from marshmallow.validate import (
    Length,
    OneOf)
from muria.entities import *
from htmllaundry import strip_markup
import uuid
import datetime


class Person_Schema(Schema):
    """Person Schema
    Mendata jenis field-field yang akan digunakan oleh entitas Person
    """
    id = fields.UUID(required=True)
    nik = fields.String(required=True)
    nama = fields.String(required=True)
    tempat_lahir = fields.String(required=True)
    tanggal_lahir = fields.Date(required=True)
    jenis_kelamin = fields.String(required=True)
    anak_ke = fields.Integer(allow_none=True)
    jum_saudara = fields.Integer(allow_none=True)
    tinggal_bersama = fields.String(allow_none=True)
    pendidikan_terakhir = fields.String(allow_none=True)
    phone1 = fields.String(allow_none=True)
    phone2 = fields.String(allow_none=True)
    pekerjaan = fields.String(allow_none=True)
    penghasilan = fields.Integer(allow_none=True)
    # tanggal_update = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    tanggal_entry = fields.Date(date)
    '''
    santri = Optional("Santri", only=['id'])
    harim = fields.Nested("Keluarga", reverse="mahram")
    mahram = fields.Nested("Keluarga", reverse="harim")
    pegawai = Optional("Pegawai_Lembaga", reverse="id")
    alamat = fields.Nested("Alamat")
    '''
    @post_load
    def nativesToStr(self, in_data):
        if isinstance(in_data['id'], uuid.UUID):
            in_data['id'] = str(in_data['id'])
        if isinstance(in_data['tanggal_entry'], datetime.date):
            in_data['tanggal_entry'] = in_data['tanggal_entry'].isoformat()[:10]
        if isinstance(in_data['tanggal_lahir'], datetime.date):
            in_data['tanggal_lahir'] = in_data['tanggal_lahir'].isoformat()[:10]
        return in_data

class Santri_Schema(Schema):
    """Santri Schema
    Sebenarnya turunan dari skema Person dengan tambahan beberapa field khusus
    """
    id = fields.UUID(required=True)
    nis = fields.String(required=True)
    wali = fields.Integer(missing=None)
    asuhan = fields.Nested("Santri_Schema", only=['id'], many=True)
    tanggal_mulai = fields.Date(required=True)
    tanggal_akhir = fields.Date(required=True)
    pengurus = fields.Integer(missing=None)
    kepala_wilayah = fields.Integer(missing=None)
    kepala_blok = fields.Integer(missing=None)
    kepala_kamar = fields.Integer(missing=None)
    #menghuni_kamar = fields.Nested("Asrama_Kamar_Schema", only=['id'])
    menghuni_kamar = fields.Integer(missing=None)
    # ----
    nik = fields.String(required=True)
    nama = fields.String(required=True)
    tempat_lahir = fields.String(required=True)
    tanggal_lahir = fields.Date(required=True)
    jenis_kelamin = fields.String(required=True)
    anak_ke = fields.String(allow_none=True)
    tinggal_bersama = fields.String(allow_none=True)
    pendidikan_terakhir = fields.String(allow_none=True)
    phone1 = fields.String(allow_none=True)
    phone2 = fields.String(allow_none=True)
    email = fields.String(missing=None, allow_none=True)
    pekerjaan = fields.String(allow_none=True)
    penghasilan = fields.Integer(allow_none=True)
    #tanggal_update = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    tanggal_entry = fields.Date()

    @post_load
    def nativesToStr(self, in_data):
        if isinstance(in_data['id'], uuid.UUID):
            in_data['id'] = str(in_data['id'])
        if isinstance(in_data['tanggal_entry'], datetime.date):
            in_data['tanggal_entry'] = in_data['tanggal_entry'].isoformat()[:10]
        if isinstance(in_data['tanggal_lahir'], datetime.date):
            in_data['tanggal_lahir'] = in_data['tanggal_lahir'].isoformat()[:10]
        return in_data


class Keluarga_Schema(Schema):
    harim = fields.Integer("Person_Schema", reverse="mahram")
    mahram = fields.Integer("Person_Schema", reverse="harim")
    relasi = fields.Integer("Hubungan_Keluarga", reverse="hubungan")


class Hubungan_Keluarga_Schema(Schema):
    hubungan = fields.Nested("Keluarga_Schema", reverse="relasi")
    nama_relasi = fields.String(required=True)
    nama_relasi_terbalik = fields.String(required=True)
    jenis_kelamin = fields.String(required=True)


class Asrama_Wilayah_Schema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    nama_wilayah = fields.String(required=True)
    kepala_wilayah = fields.String("Santri_Schema", only=['id'], allow_none=True)
    lokasi_wilayah = fields.String(allow_none=True)
    area_wilayah = fields.String(required=True)
    blok_wilayah = fields.Nested("Asrama_Blok_Schema", only=['id'], many=True)


class Asrama_Blok_Schema(Schema):
    nama_blok = fields.String(required=True)
    kepala_blok = fields.Integer("Santri_Schema")
    wilayah = fields.Integer("Asrama_Wilayah_Schema")
    kamar = fields.Nested("Asrama_Kamar_Schema")


class Asrama_Kamar_Schema(Schema):
    nama_kamar = fields.String(required=True)
    ketua_kamar = fields.String("Santri_Schema", only=['id'], allow_none=True)
    blok = fields.Integer("Asrama_Blok_Schema", only=['id'])
    jumlah_penghuni = fields.Integer(allow_none=True)
    penghuni_kamar = fields.Nested("Santri_Schema", only=['id'], many=True)


class Lembaga_Schema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String(required=True)
    nama = fields.String(required=True)
    nama_panjang = fields.String(required=True)
    lokasi = fields.String()
    keterangan = fields.String()
    pegawai = fields.Nested("Pegawai_Lembaga_Schema", only=['id'], many=True)
    jabatan = fields.Nested("Jabatan_Lembaga_Schema", only=["kode"], many=True)


class Jabatan_Lembaga_Schema(Schema): # Immutable, bisa diupdate sesuai kebutuhan
    id = fields.Integer(allow_none=True, dump_only=True)
    jabatan = fields.String(required=True)
    lembaga = fields.Integer("Lembaga_Schema_Schema", only=['id'])
    keterangan = fields.String(allow_none=True)
    #pejabat = fields.Nested("Pegawai_Lembaga_Schema", only=['id'], many=True)


class Pegawai_Lembaga_Schema(Schema):
    id = fields.String("Person_Schema", only=['id'])
    nip = fields.String(required=True) # No Induk Pegawai, buat baru bila bukan PNS
    lembaga = fields.Integer("Lembaga_Schema", only=['id'])
    jabatan = fields.Integer("Jabatan_Lembaga_Schema", only=['id'])
    pangkat = fields.String(required=True)
    catatan = fields.String(allow_none=True)
    tanggal_mulai = fields.Date()
    tanggal_akhir = fields.Date()


class Biro_Kepesantrenan_Schema(Schema):
    kode = fields.String(required=True)
    nama = fields.String(required=True, unique=True)
    lokasi = fields.String(allow_none=True)
    keterangan = fields.String(allow_none=True)
    pengurus = fields.Nested("Pengurus_Pesantren_Schema")
    jabatan = fields.Nested("Jabatan_Biro_Kepesantrenan_Schema")


class Jabatan_Biro_Kepesantrenan_Schema(Schema):
    kode = fields.String(required=True)
    jabatan = fields.String(required=True)
    keterangan = fields.String(allow_none=True)
    biro = fields.Integer("Biro_Kepesantrenan_Schema", reverse="jabatan")
    pengurus = fields.Nested("Pengurus_Pesantren_Schema")


class Pengurus_Pesantren_Schema(Schema):
    id = fields.String("Santri_Schema", reverse="pengurus")
    nip = fields.String(required=True)     # No. Induk Pengurus
    biro = fields.Integer("Biro_Kepesantrenan_Schema")
    jabatan = fields.Integer("Jabatan_Biro_Kepesantrenan_Schema")
    catatan = fields.String(allow_none=True)
    tanggal_mulai = fields.Date()
    tanggal_akhir = fields.Date()


class Jenis_Alamat_Schema(Schema):
    jenis = fields.String(required=True)
    keterangan = fields.String(allow_none=True)
    alamat = fields.Nested("Alamat_Schema")


class Alamat_Schema(Schema):
    pemilik = fields.Integer("Person_Schema", reverse="alamat")
    jenis = fields.Integer("Jenis_Alamat_Schema")
    alamat = fields.String(required=True)
    kecamatan = Optional("Alamat_Kecamatan_Schema")
    kabupaten = fields.Integer("Alamat_Kabupaten_Schema")
    provinsi = fields.Integer("Alamat_Provinsi_Schema")
    negara = fields.Integer("Alamat_Negara_Schema")
    kodepos = Optional(str)


class Alamat_Kecamatan_Schema(Schema):
    kode_kecamatan = fields.String(required=True)
    nama_kecamatan = fields.String(required=True)
    kabupaten = fields.Integer("Alamat_Kabupaten_Schema", reverse="daftar_kecamatan")
    alamat = fields.Nested("Alamat_Schema")


class Alamat_Kabupaten_Schema(Schema):
    kode_kabupaten = fields.String(required=True)
    nama_kabupaten = fields.String(required=True)
    provinsi = fields.Integer("Alamat_Provinsi_Schema", reverse="daftar_kabupaten")
    daftar_kecamatan = fields.Nested("Alamat_Kecamatan_Schema", reverse="kabupaten")
    alamat = fields.Nested("Alamat_Schema")


class Alamat_Provinsi_Schema(Schema):
    nama_provinsi = fields.String(required=True)
    kode_provinsi = fields.String(required=True)
    negara = fields.Integer("Alamat_Negara_Schema", reverse="daftar_provinsi")
    daftar_kabupaten = fields.Nested("Alamat_Kabupaten_Schema", reverse="provinsi")
    alamat = fields.Nested("Alamat_Schema")


class Alamat_Negara_Schema(Schema):
    nama_negara = fields.String(required=True)
    kode_iso = fields.String(required=True)
    daftar_provinsi = fields.Nested("Alamat_Provinsi_Schema", reverse="negara")
    alamat = fields.Nested("Alamat_Schema")


class User_Schema(Schema):
    __model__ = User

    username = fields.String(required=True, validate=Length(min=8, error="too short"))
    password = fields.String(required=True, validate=Length(min=8, error="too short"))
    email = fields.String(missing=None, allow_none=True)

    @post_load()
    def make_object(self, data):
        return self.__model__.get(username=strip_markup(data['username']), password=data['password'])


class User_Group_Schema(Schema):
    pass

'''
class alumni_Schema(Schema):
class jejak_rekam_Schema(Schema):
class khadam_Schema(Schema):
class pelajar_lembaga_Schema(Schema):
'''
