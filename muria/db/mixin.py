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
"""muria entity class."""

from datetime import datetime, date
from uuid import UUID
import types


class Mixin_Loader(object):
    schema_name = ''
    schema = None
    entity = None  # ref to the entity itself


    def init(self, myself):
        self.schema_name = eval(self.__class__.__name__ + '_Schema')
        self.schema = self.schema_name()
        self.schema.entity = myself

    def _collect(self):
        self.schema._collect()

    def getDict(self, opt=None):
        if self.schema_name == '':
            self.init(myself=self)
        self._collect()
        if opt is None:
            return self.schema.template
        else:
            return self.schema.template.get(opt)


class Base_Schema(object):
    template = {}

    def getSet(self, obj_list, opt=None):
        data = []
        if obj_list.count() > 0:
            olist = list(obj_list)
            data = [item.getDict(opt) for item in olist]
        return data


class Orang_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id.hex,
            'nik': self.entity.nik,
            'nama': self.entity.nama,
            'jinshi': self.entity.jinshi.id,
            'tempat_lahir': self.entity.tempat_lahir,
            'tanggal_lahir': self.entity.tanggal_lahir.isoformat(),
            'telepon': self.getSet(self.entity.telepon),
            'pendidikan_akhir': self.entity.pendidikan_akhir,
            'alamat': self.getSet(self.entity.alamat),
            'pekerjaan': self.entity.pekerjaan,
            'tanggal_masuk': self.entity.tanggal_masuk.isoformat()
        }


class Santri_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id.hex,
            'nik': self.entity.nik,
            'nama': self.entity.nama,
            'jinshi': self.entity.jinshi.id,
            'tempat_lahir': self.entity.tempat_lahir,
            'tanggal_lahir': self.entity.tanggal_lahir.isoformat(),
            'telepon': self.getSet(self.entity.telepon),
            'pendidikan_akhir': self.entity.pendidikan_akhir,
            'alamat': self.getSet(self.entity.alamat),
            'pekerjaan': self.entity.pekerjaan,
            'nis': self.entity.nis,
            'anak_ke': self.entity.anak_ke,
            'jumlah_saudara': self.entity.jumlah_saudara,
            'tinggal_bersama': self.entity.tinggal_bersama,
            'penanggung_biaya': self.entity.penanggung_biaya,
            'domisili': self.getSet(self.entity.domisili),
            'orang_tua': self.getSet(self.entity.orang_tua, 'ortu'),
            'hobi': self.getSet(self.entity.hobi),
            'tanggal_masuk': self.entity.tanggal_masuk.isoformat()
        }


class Ortu_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id.hex,
            'nik': self.entity.nik,
            'nama': self.entity.nama,
            'jinshi': self.entity.jinshi.id,
            'tempat_lahir': self.entity.tempat_lahir,
            'tanggal_lahir': self.entity.tanggal_lahir.isoformat(),
            'telepon': self.getSet(self.entity.telepon),
            'pendidikan_akhir': self.entity.pendidikan_akhir,
            'alamat': self.getSet(self.entity.alamat),
            'pekerjaan': self.entity.pekerjaan,
            'tanggal_tercatat': self.entity.tanggal_masuk.isoformat(),
            'pendapatan': self.entity.pendapatan,
            'anak': self.getSet(self.entity.anak, 'anak')
        }


class Alumni_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id.hex,
            'nik': self.entity.nik,
            'nama': self.entity.nama,
            'jinshi': self.entity.jinshi.id,
            'tempat_lahir': self.entity.tempat_lahir,
            'tanggal_lahir': self.entity.tanggal_lahir.isoformat(),
            'telepon': self.getSet(self.entity.telepon),
            'pendidikan_akhir': self.entity.pendidikan_akhir,
            'alamat': self.getSet(self.entity.alamat),
            'pekerjaan': self.entity.pekerjaan,
            'nis': self.entity.nis,
            'anak_ke': self.entity.anak_ke,
            'jumlah_saudara': self.entity.jumlah_saudara,
            'tinggal_bersama': self.entity.tinggal_bersama,
            'penanggung_biaya': self.entity.penanggung_biaya,
            'domisili': self.getSet(self.entity.domisili),
            'orang_tua': self.getSet(self.entity.orang_tua, 'ortu'),
            'hobi': self.getSet(self.entity.hobi),
            'tanggal_masuk': self.entity.tanggal_masuk.isoformat(),
            'tanggal_lulus': self.entity.tanggal_lulus,
            'ijazah_akhir': self.entity.ijazah_akhir.getDict()
        }


class Data_Alamat_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'jalan': self.entity.jalan,
            'kelurahan': self.entity.kelurahan.nama,
            'kecamatan': self.entity.kecamatan.nama,
            'kabupaten': self.entity.kabupaten.nama,
            'provinsi': self.entity.provinsi.nama,
            'negara': self.entity.negara.nama,
            'kode_pos': self.entity.kode_pos
        }


class Alamat_Kelurahan_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'kode': self.entity.kode,
            'nama': self.entity.nama
        }


class Alamat_Kecamatan_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'kode': self.entity.kode,
            'nama': self.entity.nama
        }

    def daftar_kelurahan(self):
        return self.getSet(self.entity.kelurahan)


class Alamat_Kabupaten_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'kode': self.entity.kode,
            'nama': self.entity.nama
        }

    def daftar_kecamatan(self):
        return self.getSet(self.entity.kecamatan)


class Alamat_Provinsi_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'kode': self.entity.kode,
            'nama': self.entity.nama
        }

    def daftar_kabupaten(self):
        return self.getSet(self.entity.kabupaten)


class Alamat_Negara_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'kode': self.entity.kode,
            'nama': self.entity.nama
        }

    def daftar_provinsi(self):
        return self.getSet(self.entity.provinsi)


class Jenis_Alamat_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def jumlah_alamat(self):
        return self.entity.alamat.count()


class Hobi_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama,
            'kategori': self.entity.kategori.nama
        }

    def jumlah_penghobi(self):
        return self.entity.hobi_santri.count()


class Kategori_Hobi_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def daftar_hobi(self):
        return self.entity.getSet(self.entity.hobi)


class Jenis_Telepon_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def jumlah_telepon(self):
        return self.entity.telepon.count()


class Asrama_Rayon_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama,
            # 'kamar': self.getSet(self.entity.kamar), # expensive query
            'area': self.entity.area.kecil,
            'jenis': self.entity.jenis.nama
        }

    def daftar_kamar(self):
        return self.entity.getSet(self.entity.kamar)


class Asrama_Kamar_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama,
            'rayon': self.entity.rayon.nama
        }

    def daftar_penghuni(self):
        return self.entity.getSet(self.entity.penghuni_kamar)


class Jenis_Asrama_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def jumlah_asrama(self):
        return self.entity.asrama.count()


class Penghuni_Kamar_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.santri.id.hex,
            'nama': self.entity.santri.nama,
            'kamar': self.entity.asrama_kamar.getDict(),
            'tanggal_masuk': self.entity.tanggal_masuk.isoformat(),
            'tanggal_keluar': self.entity.tanggal_keluar.isoformat()
        }


class Pendidikan_Akhir_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'jenjang': self.entity.jenjang.nama,
            'sekolah': self.entity.sekolah,
            'tahun': self.entity.tahun.isoformat(),
            'no_ijazah': self.entity.no_ijazah,
        }
    # NOTE:
    # Untuk menampilkan daftar keseluruhan orang/alumni dengan
    # jenjang tertentu bisa menggunakan method select bawaan pony

    def jumlah_pemilik_jenjang(self):
        return self.entity.orang.count()

    def jumlah_alumni_jenjang(self):
        return self.entity.alumni.count()


class Tingkat_Pendidikan_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama,
            'singkatan': self.entity.singkatan
        }

    def jumlah_pendidikan_akhir(self):
        return self.entity.pendidikan_akhir.count()


class Pekerjaan_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def jumlah_pekerja(self):
        return self.entity.orang.count()


class Jinshi_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama,
            'kecil': self.entity.kecil,
            'formal': self.entity.formal
        }

    def jumlah_jinshi(self):
        return self.entity.orang.count()

    def jumlah_rayon(self):
        return self.entity.rayon.count()

    def daftar_jinshi(self):
        return self.entity.getSet(self.entity.orang)

    def daftar_rayon(self):
        return self.entity.getSet(self.entity.rayon)


class Pengguna_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.orang.id.hex,
            'username': self.entity.username,
            'email': self.entity.email,
            'suspended': self.entity.suspended,
        }

    def jumlah_koneksi(self):
        return self.entity.koneksi.count()

    def jumlah_kewenangan(self):
        return self.entity.kewenangan.count()

    def daftar_koneksi(self):
        return self.entity.getSet(self.entity.koneksi)

    def daftar_kewenangan(self):
        return self.entity.getSet(self.entity.kewenangan)


class Grup_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama,
            'keterangan': self.entity.keterangan,
        }

    def daftar_wewenang(self):
        return self.getSet(self.entity.wewenang)


class Figur_Ortu_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'nama': self.entity.nama
        }

    def jumlah_figur(self):
        return self.relasi.count()


class Relasi_Schema(Base_Schema):
    def _collect(self):
        # NOTE:
        # Perlu dibuat mekanisme agar otomatis menampilkan
        # skema anak atau ortu sesuai objek yang diinginkan
        self.template = {
            'ortu': {
                str(self.entity.figur.nama_atas): {
                    'id': self.entity.ortu.id.hex,
                    'nama': self.entity.ortu.nama,
                }
            },
            'anak': {
                'id': self.entity.santri.id.hex,
                'nama': self.entity.santri.nama
            }
        }


class Telepon_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            str(self.entity.jenis.nama): {
                'id': self.entity.id,
                'nomor': self.entity.nomor,
                'orang': {
                    'id': self.entity.orang.id.hex,
                    'nama': self.entity.orang.nama
                },
                'kode_negara': self.entity.kode_negara,
                'kode_regional': self.entity.kode_regional
            }
        }


class Alamat_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'default': self.entity.default,
            str(self.entity.jenis.nama): self.entity.alamat.getDict()
        }


class Hobi_Santri_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'santri': {
                'id': self.entity.santri.id.hex,
                'nama': self.entity.santri.nama
            },
            'hobi': self.entity.hobi
        }


class Wewenang_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'nama': self.entity.nama
        }

    def jumlah_kewenangan(self):
        return self.kewenangan.count()

    def jumlah_grup(self):
        return self.grup.count()

    def daftar_kewenangan(self):
        return self.entity.getSet(self.entity.kewenangan)

    def daftar_grup(self):
        return self.entity.getSet(self.entity.grup)


class Grup_Wewenang_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'grup': self.entity.grup.nama,
            'wewenang': self.entity.wewenang.nama
        }


class Online_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'id': self.entity.id,
            'rkey': self.entity.rkey,
            'akey': self.entity.akey,
            'uakey': self.entity.uakey,
            'pengguna': {
                'id': self.entity.pengguna.orang.id.hex,
                'username': self.entity.pengguna.username
            },
            'referrer': self.entity.referrer,
            'ua': self.entity.ua,
            'loc': self.entity.loc,
            'origin': self.entity.origin,
            'time': self.entity.time.isoformat(),
            'last_time': self.entity.last_time,
            'rkey_period': self.entity.rkey_period,
            'akey_period': self.entity.akey_period,
            'offline': self.entity.offline.rkey
        }


class Offline_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'online': self.entity.online,
            'rkey': self.entity.rkey,
            'akey': self.entity.akey,
            'uakey': self.entity.uakey
        }


class Kewenangan_Schema(Base_Schema):
    def _collect(self):
        self.template = {
            'pengguna': self.entity.pengguna,
            'wewenang': self.entity.wewenang
        }
