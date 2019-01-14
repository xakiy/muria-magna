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
import re
import io
import mimetypes
import magic
from muria.init import config, logger


class FileStore(object):
    """
    Store file upload via mutlipart/form-data request.

    Currently does not support "multiple" files input,
    only save one file per field name.
    """

    # def save(self, file_id, input_handler, dest_dir):
    def save(self, input_handler, dest_dir):

        # We should sanitize dest_dir as if someone will
        # use in arbitrary way
        logger.info('Saving uploaded file...')

        tick = time.time()
        random_name = str(tick).replace('.', '') + uuid.uuid4().hex

        # Read file as binary
        raw = input_handler.file

        # Retrieve filetype
        source_type = input_handler.type
        logger.info('Source Type: {0}'.format(source_type))

        # Retrieve file extension
        source_ext = '.' + input_handler.filename.rsplit('.')[1]
        # BUG: doesn't yet support multi extension ie. .tar.gz
        logger.info('Source Ext: {0}'.format(source_ext))

        # To prevent incomplete files from being used we write it
        # first as temporary one.
        tempfile_path = os.path.join(dest_dir, random_name) + '~'
        logger.info('Temporary File Path: {0}'.format(tempfile_path))

        try:
            # Then write the stream data to that temporary file
            output_file = open(tempfile_path, 'x+b')

            shutil.copyfileobj(raw, output_file)

            # If done writing, grab the extension
            output_file.seek(0)
            extensions = mimetypes.guess_all_extensions(
                magic.from_buffer(output_file.read(128), mime=True))
            output_file.close()

            ext = source_ext if source_ext in extensions else extensions[0]
            new_filename = random_name + ext
            realfile_path = os.path.join(dest_dir, new_filename)

            # Now that we know the file has been fully saved to disk
            # and we can rename it.
            os.rename(tempfile_path, realfile_path)
            # If temp_dir and dest_dir is different filesystem
            # consider to use shutil

        except FileNotFoundError as nof:
            logger.debug('Error: {0} of "{1}"'.format(nof.strerror, new_filename))
            new_filename = None

        logger.info('Real File Path: {0}'.format(realfile_path))
        return new_filename


class ImageStore(object):

    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )

    def __init__(self, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = config.get('path', 'image_pub_dir')
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, image_stream, image_content_type):
        ext = mimetypes.guess_extension(image_content_type)
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        image_path = os.path.join(self._storage_path, name)

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name

    def open(self, name):
        # Always validate untrusted input!
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('File not found')

        image_path = os.path.join(self._storage_path, name)
        stream = self._fopen(image_path, 'rb')
        stream_len = os.path.getsize(image_path)

        return stream, stream_len
