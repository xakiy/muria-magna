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

""" muria account class. """

import falcon
from muria.resource.base import Resource
from muria.lib.misc import dumpAsJSON
from muria.db.model import Orang, Pengguna
from muria.db.schema import Pengguna_Schema
from pony.orm import db_session, ObjectNotFound, flush
from pony.orm.dbapiprovider import IntegrityError


class Accounts(Resource):

    @db_session
    def on_get(self, req, resp, **params):
        if params.get('jwt_claims') and params['jwt_claims'].get('roles'):
            pid = params['jwt_claims']['pid']
            users = Pengguna.select()[:self.config.getint('app', 'page_limit')]
            ps = Pengguna_Schema()
            if len(users) > 0:
                content = {
                    'count': len(users),
                    'accounts':
                    [ps.dump(u)[0] for u in users]}
                resp.status = falcon.HTTP_200
                resp.body = dumpAsJSON(content)
            else:
                raise falcon.HTTPNotFound(
                    description='Profile is empty',
                    code=404)
