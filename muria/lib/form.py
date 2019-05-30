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
"""Form Handler for x-www-form-urlencoded."""

from falcon import media, uri, errors
from urllib import parse


def stringify(item):
        if not isinstance(item, str) or not isinstance(item, bytes):
            return str(item)
        return item


def data_unpacks(string):
    """An alias for parse_query_string."""
    return uri.parse_query_string(string)


def data_packs(data):
    """Pack a dict into concatenated string."""
    t = list()
    for i in data:
        t.append('='.join([i, parse.quote_plus(stringify(data[i]))]))
    result = '&'.join(t)
    if not isinstance(result, bytes):
        return result.encode('utf-8')
    return result


class FormHandler(media.BaseHandler):
    """Custom Handler for 'application/x-www-form-urlencoded'."""

    def deserialize(self, stream, content_type, content_length):
        """Deserialize stream."""
        try:
            return data_unpacks(stream.read().decode('utf-8'))
        except ValueError as err:
            raise errors.HTTPBadRequest(
                'Invalid Form field',
                'Could not parse field content - {0}'.format(err)
            )

    def serialize(self, media, content_type):
        """Serialize data."""
        result = data_packs(media)
        return result
