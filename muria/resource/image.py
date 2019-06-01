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

"""muria downstreamer class."""

import falcon
from muria.init import config
from muria.resource.base import Resource
from muria.lib.misc import dumpAsJSON
from muria.lib.filestore import FileStore, ImageStore

import mimetypes
import msgpack


class Collection(Resource):
    def __init__(self):
        self._image_store = ImageStore

    def on_get(self, req, resp):
        # TODO: Modify this to return a list of href's based on
        # what images are actually available.
        doc = {"images": [{"href": "/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png"}]}

        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_201
        resp.location = "/images/" + name


class Item(Resource):
    def __init__(self):
        self._image_store = ImageStore

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        resp.stream, resp.stream_len = self._image_store.open(name)


class Upload(object):

    _fileStore = FileStore()

    def on_post(self, req, resp, **params):
        print(req.headers, req.get_param("foto"))
        # To prevent multiple repost, we need to use unique
        # id checking, like generated uuid that will be
        # compared to previous post
        # uid = req.get_param('foto_id')
        foto = req.get_param("foto")

        if foto is not None:
            # name = self._fileStore.save(uid, foto, config.get('path', 'image_pub_dir'))
            name = self._fileStore.save(foto, config.get("path", "image_pub_dir"))
            if name is not None:
                resp.status = falcon.HTTP_201
                resp.location = name
                content = {"success": "file uploaded as {0}".format(name)}
            else:
                resp.status = falcon.HTTP_404
                resp.location = None
                content = {"error": "file failed to upload"}
        else:
            resp.status = falcon.HTTP_404
            resp.location = None
            content = {"error": "upload failed"}

        resp.body = dumpAsJSON(content)
