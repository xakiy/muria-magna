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

policy_config = {
    'roles': [
        'admin',
        'manager',
        'pengguna',
    ],
    # TODO:
    # verba yang digunakan disini kurang mewakili grup dari role-role terkait
    # grup "read" mungkin lebih cocok bila diganti menjadi "umum",
    # "create" -> "creator"
    # "update" -> "kontributor"
    # "hapus" -> "editor"
    'groups': {
        'read': ['admin', 'manager', 'pengguna'],
        'create': ['admin', 'manager'],
        'update': ['admin', 'manager'],
        'delete': ['admin'],
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
        '/persons': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/persons/{id}': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/santri': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/santri/{id}': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/lembaga': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/lembaga/{lid}': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/lembaga/{lid}/jabatan': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/lembaga/{lid}/jabatan/{id}': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/wilayah': {
            'GET': ['read'],
            'POST': ['create'],
            'OPTIONS': ['@passthrough'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/wilayah/kepala': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/wilayah/{wid:int}': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/wilayah/{wid:int}/blok': {
            'GET': ['read'],
            'POST': ['create'],
            'PUT': ['update'],
            'DELETE': ['delete'],
        },
        '/stats/santri': {
            'GET': ['@any-role']
        },
        '/stats/santri/{jinshi}': {
            'GET': ['read']
        },
        '/upload': {
            'POST': ['@passthrough']
        }
    },
}
