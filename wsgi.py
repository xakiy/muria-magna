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
"""muria main app, wsgi."""

import falcon
import os

from settings import config
from settings import connection
from settings import middleware_list
# from muria import tokenizer
from muria import auth
from muria import personal
#from muria import lembaga
#from muria import asrama
#from muria import stats
#from muria import downstreamer
# from muria import devel


app = application = falcon.API(middleware=middleware_list)

app.req_options.auto_parse_form_urlencoded = True

# Fitur baru di falcon 1.4.0
app.add_static_route('/web', '/home/zakiy/public_html/giriDashboard/')
# app.add_static_route('/pub', os.path.dirname(os.path.abspath(__file__)) +
#                     '/' + config.path('storage_path'))
app.add_static_route('/ref', '/home/zakiy/public_html/sufee/')

""" Path otentikasi pengguna """
app.add_route('/auth', auth.Authentication(config))
app.add_route('/verify', auth.Verification(config))

# semua personal/warga, termasuk para santri, bahkan wali santri di rumah
app.add_route('/persons', personal.ResPersons())
# person by uuid
app.add_route('/persons/{id:uuid}', personal.ResDataPerson())

# listing data semua santri, dengan paginasi
app.add_route('/santri', personal.ResSantri())
# data santri by uuid
app.add_route('/santri/{id:uuid}', personal.ResDataSantri())
'''
# listing data semua lembaga
app.add_route('/lembaga', lembaga.ResLembaga())
# data sebuah lembaga berdasarkan slug(nick pendek)
app.add_route('/lembaga/{lid}', lembaga.ResDataLembaga())
# listing semua jabatan berdasarkan lembaga
app.add_route('/lembaga/{lid}/jabatan', lembaga.ResJabatanLembaga())
# listing semua jabatan berdasarkan lembaga
app.add_route('/lembaga/{lid}/jabatan/{id}', lembaga.ResJabatanLembagaDetail())
# listing semua karyawan berdasarkan lembaga
# app.add_route('/lembaga/{lid}/karyawan', lembaga.ResDataLembaga())
# listing semua pengurus lembaga yang berstatus santri
# app.add_route('/lembaga/karyawan/santri', lembaga.sebuahLembaga())
# listing semua pegawai lembaga yang non-santri
# app.add_route('/lembaga/karyawan/nonsantri', lembaga.sebuahLembaga())

app.add_route('/wilayah', asrama.ResWilayah())
app.add_route('/wilayah/kepala', asrama.ResKepalaWilayah())
app.add_route('/wilayah/{wid:int}', asrama.ResDataWilayah())
app.add_route('/wilayah/{wid:int}/blok', asrama.ResBlok())

# data statistik dalam angka
app.add_route('/stats/santri', stats.ResStatsSantri())
app.add_route('/stats/santri/{jinshi}', stats.ResStatsSantriByJinshi())
# app.add_route('/stats/pengurus/putra')
# app.add_route('/stats/pengurus/putri')
# app.add_route('/stats/pengurus/wilayah')
# app.add_route('/stats/pengurus/wilayah/putra')
# app.add_route('/stats/pengurus/wilayah/')

app.add_route('/upload', downstreamer.DownStream())
'''