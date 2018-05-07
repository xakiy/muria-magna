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

import time
import uuid
import shutil
import os
import mimetypes
import magic
from muria.config import conf
from falcon_cors import CORS


class FileStore(object):
    """
    Store file upload via mutlipart/form-data request.

    Currently does not support "multiple" files input,
    only save one file per field name.
    """

    _storage_path = conf.path('storage_path')

    def save(self, input_handler):

        tick = time.time()
        random_name = str(tick).replace('.', '') + uuid.uuid4().hex

        # Read file as binary
        raw = input_handler.file

        # Retrieve filetype
        source_type = input_handler.type

        # Retrieve file extension
        source_ext = '.' + input_handler.filename.rsplit('.')[1]
        # BUG: doesn't yet support multi extension ie. .tar.gz
        print(source_ext)

        # Define file_path
        file_path = os.path.join(self._storage_path, random_name)

        # Write to a temporary file to prevent incomplete files from
        # being used.
        temp_file_path = file_path + '~'

        # Finally write the data to a temporary file
        try:
            output_file = open(temp_file_path, 'x+b')
            shutil.copyfileobj(raw, output_file)

            output_file.seek(0)
            extensions = mimetypes.guess_all_extensions(
                magic.from_buffer(output_file.read(128), mime=True))
            output_file.close()

            ext = source_ext if source_ext in extensions else extensions[0]
            filename = file_path + ext

            # Now that we know the file has been fully saved to disk
            # move it into place.
            os.rename(temp_file_path, filename)

        except FileNotFoundError as nof:
            print('Error: {0} of "{1}"'.format(nof.strerror, temp_file_path))
            filename = None

        return filename
