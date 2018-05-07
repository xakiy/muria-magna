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
import magic
from muria.config import conf
from muria import libs
from falcon_cors import CORS
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget

class FileStore(object):

    _CHUNK_SIZE_BYTES = 4096

    def __init__(self):
        self._storage_path = conf.path('storage_path')


    def save(self, stream, content_type, content_length):

        if content_length:
            print(content_type, content_length)

            self.name = uuid.uuid4().hex
            self.file = os.path.join(self._storage_path, self.name)

            self.value = ValueTarget()
            self.target = FileTarget(self.file)

            self._parser = StreamingFormDataParser(headers=content_type)
            self._parser.register('name', self.value)
            self._parser.register('file', self.target)
            self._parser.register('discard-me', NullTarget())

            self._parser.data_received(stream.read())

            """
            with stream.read(self._CHUNK_SIZE_BYTES) as chunk:
                while True:
                    if not chunk:
                        break
                    self._parser.data_received(chunk)
            """

            f = open(self.file, 'rb')

            self.ext = mimetypes.guess_extension(
                magic.from_buffer(f.read(128), mime=True))

            f.close()

            self.filename = self.file + self.ext

            os.rename(self.file, self.filename)

            return self.filename
