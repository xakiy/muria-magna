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

""" muria asrama class. """

import falcon
import rapidjson as rjson
import datetime
import uuid
from muria.config import conf
from muria import libs
from muria.database import Conn
from muria.entities import Asrama_Wilayah, Asrama_Blok
from muria.schema import Asrama_Wilayah_Schema, Asrama_Blok_Schema
from pony.orm import db_session
from falcon_cors import CORS


class ResWilayah(object):
    """Resource Wilayah
    Resource ini bertanggung jawab menampilkan daftar wilayah yang ada.
    Selain itu juga menerima pembuatan resource wilayah baru.
    """
    cors = CORS(allow_origins_list=conf.sec('cors_allow_origins_list'), allow_all_headers=True, allow_all_methods=True)
    #cors = CORS(allow_all_origins=True)

    @db_session
    def on_get(self, req, resp, **params):

        print('#DEBUG @asrama')
        # DEBUG
        print('headers: ', req.headers)
        print('acc_route: ', req.access_route)
        print('params: ', req.params)
        #print('media: ', req.media)

        content = dict()
        wilayah_list = Asrama_Wilayah.select()[:conf.app('page_limit')]

        ws = Asrama_Wilayah_Schema()

        if len(wilayah_list) != 0:
            content = {'wilayah': [ ws.dump( w.to_dict() )[0] for w in wilayah_list]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'empty result'}

        resp.body = libs.dumpAsJSON(content)
        resp.etag = libs.getEtag(resp.body)

        if req.if_none_match == resp.etag:
            resp.status = falcon.HTTP_304

    def on_options(self, req, resp, **params):
        print('#DEBUG @asrama/options')
        # DEBUG
        print('headers: ', req.headers)
        print('acc_route: ', req.access_route)
        print('params: ', req.params)
        #print('media: ', req.media)
        resp.status = falcon.HTTP_OK


class ResDataWilayah(object):
    """Resouce sebuahWilayah
    Bentuk tunggal dari resouce Wilayahs
    """
    cors = CORS(allow_all_origins=conf.sec('cors_allow_all_origins'))

    @db_session
    def on_get(self, req, resp, wid, **params):

        wid = str(wid)

        if Asrama_Wilayah.exists(id=wid):
            content = Asrama_Wilayah[wid].to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Non-existant id request of #{0}'.format(id))

        resp.body = libs.dumpAsJSON(content)


class ResKepalaWilayah(object):
    """Resource Kepala Wilayah
    Resource ini bertanggung jawab menampilkan daftar para kepala wilayah.
    """
    cors = CORS(allow_all_origins=conf.sec('cors_allow_all_origins'))

    @db_session
    def on_get(self, req, resp, **params):

        content = dict()
        wilayah_list = Asrama_Wilayah.select()[:conf.app('page_limit')]

        if len(wilayah_list) != 0:

            content = {'kepala_wilayah': [{
                'id_wilayah': w.id,
                'kepala_wilayah': w.kepala_wilayah.nama,
                'kepala_wilayah_id': w.kepala_wilayah.id,
                'nama_wilayah': w.nama_wilayah,
                'area_wilayah': w.area_wilayah
            } for w in wilayah_list
            ]}

            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'empty result'}

        resp.body = libs.dumpAsJSON(content)


class ResBlok(object):
    """Resource Wilayah
    Resource ini bertanggung jawab menampilkan daftar wilayah yang ada.
    Selain itu juga menerima pembuatan resource wilayah baru.
    """
    cors = CORS(allow_all_origins=conf.sec('cors_allow_all_origins'))

    @db_session
    def on_get(self, req, resp, wid, **params):

        content = dict()
        blok_list = Asrama_Blok.select(lambda b: b.wilayah == wid)[:conf.app('page_limit')]
        bs = Asrama_Blok_Schema()

        if len(blok_list) != 0:
            content = {'blok': [ bs.dump( b.to_dict() )[0] for b in blok_list]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error':'empty result'}

        resp.body = libs.dumpAsJSON(content)


class ResDataBlok(object):
    """Resouce sebuahBlok
    Bentuk tunggal dari resouce Bloks
    """
    cors = CORS(allow_all_origins=conf.sec('cors_allow_all_origins'))

    @db_session
    def on_get(self, req, resp, id, **params):

        if Blok.exists(id=id):
            content = blok = Blok[id].to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Non-existant id request of #{0}'.format(id))

        resp.body = libs.dumpAsJSON(content)
