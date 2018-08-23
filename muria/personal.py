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

""" muria person class. """

import falcon
import rapidjson as rjson
import datetime
import uuid
from muria.resource import Resource
from muria import libs
from muria.entity import Orang, Santri
from muria.schema import Orang_Schema, Santri_Schema
from pony.orm import db_session


class ResOrangs(Resource):
    """
    Resource Orangs

    Menampilkan data person per halam
    """

    @db_session
    def on_get(self, req, resp, **params):

        content = dict()
        persons = Orang.select()[:self.config.getint('app', 'page_limit')]
        ps = Orang_Schema()
        print('personal : ', params)
        if len(persons) != 0:
            content = {
                'persons':
                [ps.dump(p.to_dict())[0] for p in persons]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'No data found!'}

        resp.body = libs.dumpAsJSON(content)


    @db_session
    def on_post(self, req, resp, **params):

        if req.media:
            ps = Orang_Schema()
            person, error = ps.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       title='Invalid Parameters',
                                       code=error)

            if not Orang.exists(nik=person['nik']):
                try:
                    pe = Orang(**person)
                    if isinstance(pe, Orang):
                        content = {'message': 'Successfully inserted',
                                   'url': '/persons/{0}'.format(pe.id)}
                        resp.status = falcon.HTTP_201
                    else:
                        content = {'message': 'Data gagal dimasukkan karena sebab yang tidak jelas :('}
                        resp.status = falcon.HTTP_400

                except err:
                    content = {'message': 'Data gagal dimasukkan'}
                    resp.status = falcon.HTTP_400
            else:
                content = {'message': 'Data orang yang bersangkutan telah ada di database'}
                resp.status = falcon.HTTP_400
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The JSON was incorrect.')

        resp.body = libs.dumpAsJSON(content)



class ResDataOrang(Resource):
    """
    Resouce dataOrang

    Berisi data pribadi masing-masing warga, diacu dengan id(uuid) mereke
    """

    @db_session
    def on_get(self, req, resp, id, **params):

        id = str(id)
        if Orang.exists(id=id):

            content = Orang[id].to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Non-existant id request of #{0}'.format(id))

        resp.body = libs.dumpAsJSON(content)



class ResSantri(Resource):
    """
    Resource Santri

    Resource ini bertanggung jawab menampilkan daftar semua santri
    berdasarkan  jumlah paging tertentu. Selain itu juga menerima
    pembuatan resource santri baru.
    """

    @db_session
    def on_get(self, req, resp, **params):

        content = dict()
        # santri_list = Santri.select()[:config.get('app', 'page_limit')]
        santri_list = Santri.select()[:self.config.getint('app', 'page_limit')]
        # paging akan disesuaikan menurut request
        sc = Santri_Schema()

        if len(santri_list) != 0:
            content = {'santri': [ sc.dump( s.to_dict() )[0] for s in santri_list]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'empty result'}

        resp.body = libs.dumpAsJSON(content)



    @db_session
    def on_post(self, req, resp, **params):

        if req.media:
            ss = Santri_Schema()
            fulan, error = ss.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       title='Invalid Parameters',
                                       code=error)

            if not Santri.exists(nis=fulan['nis']):
                try:
                    santri = Santri(**fulan)
                    if isinstance(santri, Santri):
                        content = {'message': 'Successfully inserted',
                                   'url': '/santri/{0}'.format(santri.id)}
                        resp.status = falcon.HTTP_201
                    else:
                        raise falcon.HTTPError(falcon.HTTP_500,
                                               title=falcon.HTTP_500,
                                               description="Unable to insert data")
                except err:
                    content = {'message': 'Data gagal dimasukkan'}
                    resp.status = falcon.HTTP_400
            else:
                content= {'message': 'Data orang yang bersangkutan telah ada di database'}
                resp.status = falcon.HTTP_400
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The JSON was incorrect.')

        resp.body = libs.dumpAsJSON(content)


class ResDataSantri(Resource):
    """
    Resource Seorang Santri

    Dalama Bahasa Indonesia baik secara maknawi maupun secara eksplisit bentuk tunggal
    hanya bisa dibedakan dengan manambahkan kata keterangan sebelum kata benda tersebut
    """

    @db_session
    def on_get(self, req, resp, id, **params):
        if Santri.exists(id=id):
            content = Santri[id].to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Invalid id #{0}'.format(id))

        resp.body = libs.dumpAsJSON(content)
