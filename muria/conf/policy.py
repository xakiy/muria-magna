"""muria access policy config file."""

# Copyright 2017 Ahmad Ghulam Zakiy. <ghulam (dot) zakiy (at) gmail.com>
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

# from falcon_policy import RoleBasedPolicy

Policy_Config = {
    # Roles atau peran adalah kewenangan seorang pengguna terhadap sebuah resource.
    # Seorang pengguna bisa memiliki lebih dari satu kewenangan/peran/role.
    # Catatan: menyesuaikan dengan makeWewenang di berkas premise.py
    'roles': [
        'root',
        'admin',
        'editor',
        'kontributor',
        'santriwan',
        'santriwati',
        'wali',
        'umum'
    ],
    #  Group lebih berupa jabatan kepengurusan terhadap suatu resource.
    'groups': {
        'reader': ['root', 'admin', 'editor', 'kontributor', 'santriwan', 'santriwati', 'wali', 'umum'],
        'creator': ['root', 'admin', 'editor', 'kontributor'],
        'editor': ['root', 'admin', 'editor'],
        'deleter': ['root', 'admin']
    },
    'routes': {
        '/v1/auth': {
            'GET': ['@passthrough'],
            'HEAD': ['@passthrough'],
            'OPTIONS': ['@passthrough'],
            'POST': ['@passthrough']
        },
        '/v1/auth/verify': {
            'OPTIONS': ['@passthrough'],
            # 'GET': ['@passthrough'], # phusion server would hangup if this invoked
            # TODO:
            # Bila @passthrough maka itu membuka celah bagi siapa saja bahkan cracker untuk melakukan
            # verifiksi token.
            # Karena bagaimana pun, sebelum verifikasi berlangsung, RBAC middleware
            # akan bekerja terlebih dahulu sebelum custom verifikasi token terjadi.
            'POST': ['@passthrough']
        },
        '/v1/auth/refresh': {
            'OPTIONS': ['@passthrough'],
            # TODO:
            # Idem dengan di atas.
            'POST': ['@passthrough']
        },
        '/v1/accounts': {
            'OPTIONS': ['@passthrough'],
            'GET': ['editor'],
            'POST': ['editor'],
            'PATCH': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/accounts/{id:uuid}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['editor'],
            'POST': ['editor'],
            'PATCH': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/profile': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['reader'],
            'PATCH': ['reader']
        },
        '/v1/profile/security': {
            'OPTIONS': ['@passthrough'],
            'POST': ['reader'],
            'PATCH': ['reader']
        },
        '/v1/profile/picture': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'PUT': ['reader']
        },
        '/v1/orang': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader']
        },
        '/v1/orang/{id:uuid}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/santri': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader']
        },
        '/v1/santri/{id:uuid}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/lembaga': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/lembaga/{lid}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/lembaga/{lid}/jabatan': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/lembaga/{lid}/jabatan/{id}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/rayon': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'OPTIONS': ['@passthrough'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/rayon/kepala': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/rayon/{wid:int}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/rayon/{wid:int}/blok': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/v1/stats/orang': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader']
        },
        '/v1/stats/wali': {
            'OPTIONS': ['@passthrough'],
            'GET': ['reader']
        },
        '/v1/stats/santri': {
            'OPTIONS': ['@passthrough'],
            'GET': ['@passthrough']
        },
        '/v1/stats/santri/{jinshi}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['@passthrough']
        },
        '/v1/upload': {
            'OPTIONS': ['@passthrough'],
            'POST': ['@passthrough']
        },
        '/v1/images': {
            'OPTIONS': ['@passthrough'],
            'GET': ['@passthrough']
        },
        '/v1/images/{name}': {
            'OPTIONS': ['@passthrough'],
            'GET': ['@passthrough'],
            'POST': ['@passthrough']
        }
    },
}
