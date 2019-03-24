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

""" muria lembaga class. """

import falcon
import datetime
import uuid
from muria.resource.base import Resource
from muria.lib.misc import dumpAsJSON, getEtag
from muria.db.model import Lembaga, Jabatan_Lembaga, Pegawai_Lembaga
from muria.db.schema import Lembaga_Schema, Jabatan_Lembaga_Schema, Pegawai_Lembaga_Schema
from pony.orm.core import TransactionIntegrityError, CacheIndexError


class ResLembaga(Resource):
    """Resource Lembaga
    Resource ini bertanggung jawab menampilkan daftar lembaga yang ada,
    termasuk menerima pembuatan resource lembaga baru.
    """

    @db_session
    def on_get(self, req, resp, **params):

        content = dict()
        lembaga_list = Lembaga.select()[:self.config.getint('app', 'page_limit')]
        ls = Lembaga_Schema()

        if len(lembaga_list) != 0:
            content = {'lembaga': [ ls.dump( l.to_dict() )[0] for l in lembaga_list]}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'No lembaga found!'}

        resp.body = dumpAsJSON(content)


    @db_session()
    def on_post(self, req, resp, **params):

        if req.media:
            ls = Lembaga_Schema()
            instansi, error = ls.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       title='Invalid Parameters',
                                       code=error)

            if not Lembaga.exists(lambda l: l.slug==instansi['slug'] or l.nama==instansi['nama'] or l.id==instansi['id']):
                try:
                    lembaga = Lembaga(**instansi)

                    if isinstance(lembaga, Lembaga):
                        content = {'message': 'Successfully inserted',
                                   'url': '/lembaga/{0}'.format(lembaga.id)}
                        resp.status = falcon.HTTP_201
                    else:
                        raise falcon.HTTPError(falcon.HTTP_500,
                                       title=falcon.HTTP_500,
                                       description="Unable to insert data")

                except (TransactionIntegrityError, CacheIndexError):
                    content = {'message': 'Data gagal dimasukkan'}
                    resp.status = falcon.HTTP_400
            else:
                content= {'message': 'Data tersebut telah ada di database'}
                resp.status = falcon.HTTP_400
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The JSON was incorrect.')

        resp.body = dumpAsJSON(content)


class ResDataLembaga(Resource):
    """Resouce dataLembaga
    Bentuk tunggal dari resouce Lembagas
    """

    @db_session
    def on_get(self, req, resp, lid, **params):

        if Lembaga.exists(id=lid):
            content = Lembaga.get(id=lid).to_dict()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'Resouce not found, eg. #{0}'.format(lid)}

        resp.body = dumpAsJSON(content)

    @db_session()
    def on_put(self, req, resp, **params):

        if req.media:
            ls = Lembaga_Schema()
            instansi, error = ls.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       title='Invalid Parameters',
                                       code=error)

            if Lembaga.exists(lambda l: l.slug==instansi['slug'] or l.nama==instansi['nama'] or l.id==instansi['id']):
                try:
                    lembaga = Lembaga.get(lambda l: l.slug==instansi['slug'] or l.nama==instansi['nama'] or l.id==instansi['id'])
                    lembaga.set(**instansi)

                    if isinstance(lembaga, Lembaga):
                        content = {'message': 'Successfully updated',
                                   'url': '/lembaga/{0}'.format(lembaga.id)}
                        resp.status = falcon.HTTP_201
                    else:
                        raise falcon.HTTPError(falcon.HTTP_500,
                                       title=falcon.HTTP_500,
                                       description="Unable to insert data")

                except (TransactionIntegrityError, CacheIndexError):
                    content = {'message': 'Data gagal diperbarui'}
                    resp.status = falcon.HTTP_400
            else:
                content= {'message': 'Data tersebut tidak ada di database'}
                resp.status = falcon.HTTP_400
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The JSON was incorrect.')

        resp.body = dumpAsJSON(content)


class ResJabatanLembaga(Resource):
    """Resource Lembaga
    Resource ini bertanggung jawab menampilkan daftar lembaga yang ada,
    termasuk menerima pembuatan resource lembaga baru.
    """

    @db_session
    def on_get(self, req, resp, lid, **params):

        if Lembaga.exists(id=lid):
            content = dict()
            jabatan_lembaga_list = Jabatan_Lembaga.select(lambda j: j.lembaga.id == lid)[:self.config.getint('app', 'page_limit')]
            jls = Jabatan_Lembaga_Schema()

            content = {'jabatan': [ jls.dump( jl.to_dict() )[0] for jl in jabatan_lembaga_list]}
            resp.status = falcon.HTTP_200
            resp.set_header('Access-Control-Allow-Origin','*')
        else:
            resp.status = falcon.HTTP_404
            content = {'error': 'No lembaga found!'}

        resp.body = dumpAsJSON(content)


    @db_session
    def on_post(self, req, resp, lid, **params):

        if req.media:
            jls = Jabatan_Lembaga_Schema()
            tugas, error = jls.load(req.media)

            if error:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       title='Invalid Parameters',
                                       code=error)

            if int(lid) != int(tugas['lembaga']):
                raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Cross id submitted. The JSON was incorrect.')

            if ( Lembaga.exists(id=lid) == True ) & ( Jabatan_Lembaga.exists(lembaga=tugas['lembaga'], jabatan=tugas['jabatan']) == False ):
                try:
                    jabatan = Jabatan_Lembaga(**tugas)
                    if isinstance(jabatan, Jabatan_Lembaga):
                        content = {'message': 'Data berhasil dimasukkan'}
                        resp.status = falcon.HTTP_201
                    else:
                        raise falcon.HTTPError(falcon.HTTP_500,
                                       title=falcon.HTTP_500,
                                       description="Error instansiasi entitas!")

                except:
                    content = {'message': 'Data gagal dimasukkan'}
                    resp.status = falcon.HTTP_400
            else:
                content= {'message': 'Data tersebut telah ada di database'}
                resp.status = falcon.HTTP_400
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The JSON was incorrect.')

        resp.body = dumpAsJSON(content)


class ResJabatanLembagaDetail(Resource):
    """Resource Lembaga
    Resource ini bertanggung jawab menampilkan daftar lembaga yang ada,
    termasuk menerima pembuatan resource lembaga baru.
    """

    @db_session
    def on_get(self, req, resp, lid, id, **params):

        if Lembaga.exists(id=lid) & Jabatan_Lembaga.exists(id=id):
            content = dict()
            instansi = Lembaga.get(id=lid)
            jabatan = Jabatan_Lembaga.get(id=id, lembaga=instansi.id)

            if jabatan :
                content = {'jabatan': jabatan.to_dict() }
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin','*')
            else:
                resp.status = falcon.HTTP_404
                content = {'error': 'No jabatan found!'}
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid request','Data not found!')

        resp.body = dumpAsJSON(content)


class ResKaryawanLembaga(Resource):
    pass
