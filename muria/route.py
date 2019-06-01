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

"""Route of Resources."""

from muria.resource import auth
from muria.resource import account
from muria.resource import profile
from muria.resource import personal

# from muria.resource import lembaga
from muria.resource import asrama
from muria.resource import stats
from muria.resource import uploader
from muria.resource import image
from muria.resource import oauth2

# from muria.resource import devel

base_path = "/v1"
static_route = []
resource_route = []

# Fitur baru di falcon 1.4.0
# static_route.append(('/web', '/home/zakiy/public_html/giriDashboard/'))
# static_route.append('/pub', os.path.dirname(os.path.abspath(__file__)) +
#                     '/' + config.path('storage_path'))
static_route.append(("/ref", "/home/zakiy/public_html/sufee/"))

""" Path otentikasi pengguna """
resource_route.append(("/auth", auth.Authentication()))
resource_route.append(("/auth/verify", auth.Verification()))
resource_route.append(("/auth/refresh", auth.Refresh()))

resource_route.append(("/profile", profile.Profile()))
resource_route.append(("/profile/security", profile.Security()))
resource_route.append(("/profile/picture", profile.Picture()))

resource_route.append(("/accounts", account.Accounts()))
# resource_route.append(('/accounts/{id:uuid}', res_account))

# semua personal/warga, termasuk para santri, bahkan wali santri di rumah
resource_route.append(("/orang", personal.ResOrangs()))
# person by uuid
resource_route.append(("/orang/{id:uuid}", personal.ResDataOrang()))

# listing data semua santri, dengan paginasi
resource_route.append(("/santri", personal.ResSantri()))
# data santri by uuid
resource_route.append(("/santri/{id:uuid}", personal.ResDataSantri()))
"""
# listing data semua lembaga
resource_route.append(('/lembaga', lembaga.ResLembaga()))
# data sebuah lembaga berdasarkan slug(nick pendek)
resource_route.append(('/lembaga/{lid}', lembaga.ResDataLembaga()))
# listing semua jabatan berdasarkan lembaga
resource_route.append(('/lembaga/{lid}/jabatan', lembaga.ResJabatanLembaga()))
# listing semua jabatan berdasarkan lembaga
resource_route.append(('/lembaga/{lid}/jabatan/{id}', lembaga.ResJabatanLembagaDetail()))
# listing semua karyawan berdasarkan lembaga
# resource_route.append(('/lembaga/{lid}/karyawan', lembaga.ResDataLembaga()))
# listing semua pengurus lembaga yang berstatus santri
# resource_route.append(('/lembaga/karyawan/santri', lembaga.sebuahLembaga()))
# listing semua pegawai lembaga yang non-santri
# resource_route.append(('/lembaga/karyawan/nonsantri', lembaga.sebuahLembaga()))
"""
resource_route.append(("/rayon", asrama.ResRayon()))
"""
resource_route.append(('/wilayah/kepala', asrama.ResKepalaWilayah()))
resource_route.append(('/wilayah/{wid:int}', asrama.ResDataWilayah()))
resource_route.append(('/wilayah/{wid:int}/blok', asrama.ResBlok()))
"""
# data statistik dalam angka
resource_route.append(("/stats/orang", stats.ResStatsOrang()))
resource_route.append(("/stats/wali", stats.ResStatsWali()))
resource_route.append(("/stats/santri", stats.ResStatsSantri()))
resource_route.append(
    ("/stats/santri/{jinshi}", stats.ResStatsSantriByJinshi())
)
"""
# resource_route.append(('/stats/pengurus/putra'))
# resource_route.append(('/stats/pengurus/putri'))
# resource_route.append(('/stats/pengurus/wilayah'))
# resource_route.append(('/stats/pengurus/wilayah/putra'))
# resource_route.append(('/stats/pengurus/wilayah/'))
"""
resource_route.append(("/upload", uploader.Upload()))
resource_route.append(("/images/", image.Collection()))
resource_route.append(("/images/{name}", image.Item()))

resource_route.append(("/oauth2", oauth2.Oauth2()))
