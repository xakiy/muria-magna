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
        '/auth': {
            'GET': ['@passthrough'],
            'HEAD': ['@passthrough'],
            'OPTIONS': ['@passthrough'],
            'POST': ['@passthrough']
        },
        '/auth/verify': {
            # 'GET': ['@passthrough'], # phusion server would hangup if this invoked
            # TODO:
            # Bila @passthrough maka itu membuka celah bagi siapa saja bahkan cracker untuk melakukan
            # verifiksi token.
            # Karena bagaimana pun, sebelum verifikasi berlangsung, RBAC middleware
            # akan bekerja terlebih dahulu sebelum custom verifikasi token terjadi.
            'POST': ['@passthrough']
        },
        '/auth/refresh': {
            # TODO:
            # Idem dengan di atas.
            'POST': ['@passthrough']
        },
        '/persons': {
            'GET': ['reader']
        },
        '/persons/{id:uuid}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/santri': {
            'GET': ['reader']
        },
        '/santri/{id:uuid}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/lembaga': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/lembaga/{lid}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/lembaga/{lid}/jabatan': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/lembaga/{lid}/jabatan/{id}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/rayon': {
            'GET': ['reader'],
            'POST': ['creator'],
            'OPTIONS': ['@passthrough'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/rayon/kepala': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/rayon/{wid:int}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/rayon/{wid:int}/blok': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/stats/santri': {
            'GET': ['@any-role']
        },
        '/stats/santri/{jinshi}': {
            'GET': ['reader']
        },
        '/upload': {
            'POST': ['@passthrough']
        }
    },
}
