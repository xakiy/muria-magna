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
import mimetypes
import hashlib
from muria.init import config, tokenizer
from muria.resource.base import Resource
from muria.lib.misc import getEtag, dumpAsJSON
from muria.db.model import Orang, Pengguna
from muria.db.schema import Pengguna_Schema
from muria.lib.filestore import FileStore
from pony.orm import db_session, ObjectNotFound, flush
from pony.orm.dbapiprovider import IntegrityError
import io
import os


class Profile(Resource):

    @db_session
    def on_get(self, req, resp, **params):
        if params.get('jwt_claims') and params['jwt_claims'].get('pid'):
            try:
                pid = params['jwt_claims']['pid']
                profile = Pengguna[pid]
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)

            if isinstance(profile, Pengguna):
                content = {'account': Pengguna_Schema().dump(profile)[0]}
                resp.status = falcon.HTTP_OK
                resp.body = dumpAsJSON(content)
                return

        raise falcon.HTTPNotFound(
            description='Profile is empty',
            code=404)

    @db_session
    def on_patch(self, req, resp, **params):
        if req.media.get('id') == params['jwt_claims'].get('pid'):
            try:
                user = Pengguna[params['jwt_claims'].get('pid')]
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)
            ps = Pengguna_Schema()
            update, error = ps.load(req.media)
            print(req.media, update, error)
            if error:
                raise falcon.HTTPUnprocessableEntity(
                    title='Profile Update Error',
                    description={'data': req.media, 'errors': error},
                    code=422)
            try:
                user.set(**update)
                flush()
                content = {'account': ps.dump(user)[0]}
                resp.status = falcon.HTTP_OK
                resp.body = dumpAsJSON(content)
            except (TypeError, ValueError, IntegrityError) as err:
                raise falcon.HTTPUnprocessableEntity(
                    title='Profile Update Error',
                    description=str(err), code=422)
        else:
            raise falcon.HTTPUnprocessableEntity(
                title='Profile Update Error',
                description='Incomplete data supplied',
                code=422)


class Picture(Resource):

    profile_pict_dir = config.get('path', 'profile_pict_dir')
    file_store = FileStore()

    @db_session
    def on_get(self, req, resp, **params):
        if params.get('jwt_claims') and params['jwt_claims'].get('pid'):
            try:
                pid = params['jwt_claims']['pid']
                profile = Pengguna[pid]
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)

            if isinstance(profile, Pengguna) and profile.picture:
                resp.status = falcon.HTTP_OK
                resp.stream, resp.stream_len, resp.content_type = self._open(profile.picture)

        else:
            raise falcon.HTTPUnprocessableEntity(
                title='Profile Update Error',
                description='Incomplete data supplied',
                code=422)

    @db_session
    def on_put(self, req, resp, **params):

        # To prevent multiple repost, we need to use unique
        # id checking, like generated uuid that will be
        # compared to previous post
        # uid = req.get_param('foto_id')
        foto = req.get_param('foto')
        print(foto, req.headers, req.uri)
        if foto is not None:
            # name = self._fileStore.save(uid, foto, config.get('path', 'image_pub_dir'))
            name = self.file_store.save(foto, self.profile_pict_dir)
            if name is not None:
                resp.status = falcon.HTTP_201
                resp.location = req.uri
                content = {'success': "file uploaded as {name}".format(name=name)}
            else:
                resp.status = falcon.HTTP_404
                resp.location = None
                content = {'error': "file failed to upload"}
        else:
            resp.status = falcon.HTTP_404
            resp.location = None
            content = {'error': "upload failed"}

        resp.body = dumpAsJSON(content)

    def _open(self, picture):
        try:
            path = os.path.join(config.get('path', 'profile_pict_dir'), picture)
            stream_data = open(path, 'rb')
            stream_len = os.path.getsize(path)
            stream_type = mimetypes.guess_type(path)[0]
        except FileNotFoundError as err:
            # Should return default Blank/Not found picture
            return (None, None, None)
        else:
            return (stream_data, stream_len, stream_type)

    def _getEtag(self, fileHandler):
        md5 = hashlib.md5()
        while True:
            data = fileHandler.read(2**20)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


class Security(Resource):

    @db_session
    def on_patch(self, req, resp, **params):
        if req.media.get('new_password') and req.media.get('old_password'):
            pid = params['jwt_claims'].get('pid')
            old_pass = req.media.get('old_password')
            new_pass = req.media.get('new_password')

            # calculate if new pass is 64 bit lengths
            # reject if empty
            if len(new_pass) < 64 or len(old_pass) < 64:
                raise falcon.HTTPUnprocessableEntity(
                    title="Password Change",
                    description="Invalid password length, should be 64 digits",
                    code=422)
            try:
                user = Pengguna.get(orang=pid)
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)

            if user.checkPassword(old_pass):
                salt, hashed = tokenizer.createSaltedPassword(new_pass)
                user.salt = salt
                user.password = hashed
                resp.status = falcon.HTTP_CREATED
            else:
                raise falcon.HTTPUnprocessableEntity(
                    title="Password Change",
                    description="Wrong password supplied.",
                    code=422)
