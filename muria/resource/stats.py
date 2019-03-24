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

"""muria statistics class."""

import falcon
import datetime
import uuid
from muria.resource.base import Resource
from muria.lib.misc import dumpAsJSON, getEtag
from muria.db.model import Orang, Ortu, Santri
from pony.orm import db_session, count


class ResStatsOrang(Resource):
    """Resource Statistiks Santri
    Menampilkan data statistiks jumlah total santri aktif.
    """

    @db_session
    def on_get(self, req, resp, **params):

        orang_total = count(s for s in Orang)

        if orang_total != 0:

            content = {'statistiks_orang': orang_total}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Stats error!')

        resp.body = dumpAsJSON(content)
        resp.etag = getEtag(resp.body)

        if req.if_none_match == resp.etag:
            resp.status = falcon.HTTP_304


class ResStatsWali(Resource):
    """Resource Statistiks Wali Santri
    Menampilkan data statistiks jumlah total wali santri.
    """

    @db_session
    def on_get(self, req, resp, **params):

        ortu_total = count(s for s in Ortu)

        if ortu_total != 0:

            content = {'statistiks_wali': ortu_total}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Stats error!')

        resp.body = dumpAsJSON(content)
        resp.etag = getEtag(resp.body)

        if req.if_none_match == resp.etag:
            resp.status = falcon.HTTP_304


class ResStatsSantri(Resource):
    """Resource Statistiks Santri
    Menampilkan data statistiks jumlah total santri aktif.
    """

    @db_session
    def on_get(self, req, resp, **params):

        santri_total = count(s for s in Santri)

        if santri_total != 0:

            content = {'statistiks_santri': santri_total}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            content = ('Stats error!')

        resp.body = dumpAsJSON(content)
        resp.etag = getEtag(resp.body)

        if req.if_none_match == resp.etag:
            resp.status = falcon.HTTP_304


class ResStatsSantriByJinshi(Resource):
    """Resource Statistiks Santri by Jinshi
    Menampilkan data statistiks santri berdasarkan jenis kelamin.
    """

    @db_session
    def on_get(self, req, resp, jinshi='', **params):

        try:
            if jinshi == 'putra':
                total = count(s for s in Santri if s.jinshi.id == 'l')
                key = 'statistiks_santri_putra'
            elif jinshi == 'putri':
                total = count(s for s in Santri if s.jinshi.id == 'p')
                key = 'statistiks_santri_putri'

            content = {key: total}
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_404
            content = ('Invalid Resource Request: #{0}'.format(jinshi))

        resp.body = dumpAsJSON(content)
        resp.etag = getEtag(resp.body)
