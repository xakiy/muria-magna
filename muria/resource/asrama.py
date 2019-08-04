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
import datetime
import uuid
from muria.lib.misc import getEtag
from muria.resource.base import Resource
from muria.db.model import Asrama_Rayon
from muria.db.schema import Asrama_Rayon_Schema
from pony.orm import db_session


class ResRayon(Resource):
    """Resource Rayon
    Resource ini bertanggung jawab menampilkan daftar rayon yang ada.
    Selain itu juga menerima pembuatan resource rayon baru.
    """

    @db_session
    def on_get(self, req, resp, **params):

        print("#DEBUG @asrama")
        # DEBUG
        print("headers: ", req.headers)
        print("acc_route: ", req.access_route)
        print("params: ", req.params)
        # print('media: ', req.media)

        content = dict()
        rayon_list = Asrama_Rayon.select()[: self.config.getint("app", "page_limit")]

        ars = Asrama_Rayon_Schema()

        if len(rayon_list) != 0:
            content = {"rayon": [r.getDict() for r in rayon_list]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {"error": "empty result"}

        resp.media = content
        resp.etag = getEtag(resp.media)

        if req.if_none_match == resp.etag:
            resp.status = falcon.HTTP_304

    def on_options(self, req, resp, **params):
        print("#DEBUG @asrama/options")
        # DEBUG
        print("headers: ", req.headers)
        print("acc_route: ", req.access_route)
        print("params: ", req.params)
        # print('media: ', req.media)
        resp.status = falcon.HTTP_OK


class ResDataRayon(Resource):
    """Resouce sebuahRayon
    Bentuk tunggal d ari resouce Rayons
    """

    @db_session
    def on_get(self, req, resp, wid, **params):

        wid = str(wid)

        if Asrama_Rayon.exists(id=wid):
            content = Asrama_Rayon[wid].to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = "Non-existant id request of #{0}".format(id)

        resp.media = content


class ResKepalaRayon(Resource):
    """Resource Kepala Rayon
    Resource ini bertanggung jawab menampilkan daftar para kepala rayon.
    """

    @db_session
    def on_get(self, req, resp, **params):

        content = dict()
        rayon_list = Asrama_Rayon.select()[: self.config.getint("app", "page_limit")]

        if len(rayon_list) != 0:

            content = {
                "kepala_rayon": [
                    {
                        "id_rayon": w.id,
                        "kepala_rayon": w.kepala_rayon.nama,
                        "kepala_rayon_id": w.kepala_rayon.id,
                        "nama_rayon": w.nama_rayon,
                        "area_rayon": w.area_rayon,
                    }
                    for w in rayon_list
                ]
            }

            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {"error": "empty result"}

        resp.media = content
