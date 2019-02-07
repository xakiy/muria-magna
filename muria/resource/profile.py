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

    pict_dir = config.get('path', 'profile_pict_dir')
    file_store = FileStore()

    @db_session
    def on_get(self, req, resp, **params):
        if params.get('jwt_claims') and params['jwt_claims'].get('pid'):
            try:
                pid = params['jwt_claims']['pid']
                user_profile = Pengguna[pid]
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)

            if user_profile.picture:
                resp.status = falcon.HTTP_OK
                (resp.stream,
                 resp.stream_len,
                 resp.content_type) = self._open_file(user_profile.picture)

        else:
            raise falcon.HTTPUnprocessableEntity(
                title='Profile Update Error',
                description='Incomplete data supplied',
                code=422)

    @db_session
    def on_put(self, req, resp, **params):

        if params.get('jwt_claims') and params['jwt_claims'].get('pid'):
            try:
                pid = params['jwt_claims']['pid']
                user_profile = Pengguna[pid]
            except ObjectNotFound:
                raise falcon.HTTPUnauthorized(code=401)

            # TODO:
            # To prevent multiple repost, we need to use unique
            # id checking, like generated uuid that will be
            # compared to previous post
            # uid = req.get_param('profile_image_id')
            profile_image = req.get_param('profile_image')

            if profile_image is not None:
                name = self.file_store.save(profile_image, self.pict_dir)
                if name is not None:
                    if user_profile.picture is not None:
                        self.file_store.delete(user_profile.picture)
                    resp.status = falcon.HTTP_201
                    resp.location = req.uri
                    user_profile.picture = name
                    flush()
                    content = {
                        'success':
                        "{0} file uploaded".format(os.path.basename(name))}
                else:
                    resp.status = falcon.HTTP_404
                    resp.location = None
                    content = {'error': "file failed to upload"}
            else:
                resp.status = falcon.HTTP_404
                resp.location = None
                content = {'error': "upload failed"}

            resp.body = dumpAsJSON(content)
        else:
            raise falcon.HTTPUnprocessableEntity(
                title='Profile Update Error',
                description='Incomplete data supplied',
                code=422)

    def _open_file(self, picture):
        print(picture)
        if os.path.exists(picture) and os.path.isfile(picture):
            try:
                stream_data = open(picture, 'rb')
                stream_len = os.path.getsize(picture)
                stream_type = mimetypes.guess_type(picture)[0]
                print('got it')
                return (stream_data, stream_len, stream_type)
            except FileNotFoundError as err:
                # Should return default Blank/Not found picture
                print('nee')
                pass
        print('naa')
        return (None, None, None)


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
            if not (8 <= len(new_pass) <= 40) or not (8 <= len(old_pass) <= 40):
                raise falcon.HTTPUnprocessableEntity(
                    title="Password Change",
                    description="Invalid password length, at least 8 and not more than 40 characters",
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
