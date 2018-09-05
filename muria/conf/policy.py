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
    'roles': [
        'admin',
        'manager',
        'pengguna',
        'santriwan'
    ],
    # TODO:
    # verba yang digunakan disini kurang mewakili grup dari role-role terkait
    # grup "read" mungkin lebih cocok bila diganti menjadi "umum",
    # "create" -> "creator"
    # "update" -> "kontributor"
    # "hapus" -> "editor"
    'groups': {
        'reader': ['admin', 'manager', 'pengguna', 'santriwan'],
        'creator': ['admin', 'manager', 'pengguna'],
        'editor': ['admin', 'manager'],
        'deleterr': ['admin']
    },
    'routes': {
        '/auth': {
            'GET': ['@passthrough'],
            'HEAD': ['@passthrough'],
            'OPTIONS': ['@passthrough'],
            'POST': ['@passthrough']
        },
        '/verify': {
            'GET': ['@any-role'],
            'POST': ['@any-role']
        },
        '/refresh': {
            'GET': ['@any-role'],
            'POST': ['@any-role']
        },
        '/persons': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/persons/{id:uuid}': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
        },
        '/santri': {
            'GET': ['reader'],
            'POST': ['creator'],
            'PUT': ['editor'],
            'DELETE': ['deleter'],
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
