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
import rapidjson as rjson
import uuid
import re
import io
import os
import mimetypes
from muria.config import conf
from muria.lib.misc import dumpAsJSON
from muria.filestore import FileStore
from falcon_cors import CORS
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget


class DownStream(object):

    cors = CORS(allow_all_origins=config.get('cors', 'allow_all_origins'))
    _fileStore = FileStore()

    def xon_post(self, req, resp, **params):
        import shutil
        # Retrieve input_file
        input_file = req.get_param('foto')

        # Retrieve filename
        filename = input_file.filename

        # Define file_path
        file_path = os.path.join('/home/zakiy/appForge/muria/pub', filename)

        # Write to a temporary file to prevent incomplete files from
        # being used.
        temp_file_path = file_path + '~'

        # Finally write the data to a temporary file
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file.file, output_file)

        # Now that we know the file has been fully saved to disk
        # move it into place.
        os.rename(temp_file_path, file_path)

        resp.status = falcon.HTTP_201

    def on_post(self, req, resp, **params):
        print(req.headers, req.params)
        foto = req.get_param('foto')

        if foto is not None:
            name = self._fileStore.save(foto)

            if name is not None:
                resp.status = falcon.HTTP_201
                resp.location = name
                content = {'success': "file uploaded as {0}".format(name)}
            else:
                resp.status = falcon.HTTP_404
                resp.location = None
                content = {'error': "file failed to upload"}
        else:
            resp.status = falcon.HTTP_404
            resp.location = None
            content = {'error': "upload failed"}

        resp.body = dumpAsJSON(content)
