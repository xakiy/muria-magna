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
import rapidjson as rjson
import datetime
import uuid
from muria.resource import Resource
from muria import libs
from muria.entity import Orang, Santri
from pony.orm import db_session, count


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

        resp.body = libs.dumpAsJSON(content)
        resp.etag = libs.getEtag(resp.body)

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
                total = count(s for s in Santri if s.jenis_kelamin == 'L')
                key = 'statistiks_santri_putra'
            elif jinshi == 'putri':
                total = count(s for s in Santri if s.jenis_kelamin == 'P')
                key = 'statistiks_santri_putri'

            content = {key: total}
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_404
            content = ('Invalid Resource Request: #{0}'.format(jinshi))

        resp.body = libs.dumpAsJSON(content)
        resp.etag = libs.getEtag(resp.body)
