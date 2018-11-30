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
"""Pustaka Umum."""

import datetime
import collections

from muria.init import config, DEBUG


try:
    import rapidjson as json
except ModuleNotFoundError:
    import json
    class DatetimeEncoder(json.JSONEncoder):
        """Encoder pengubah datetime sebagai string biasa."""

        def default(self, obj):
            if isinstance(obj, datetime.datetime) or \
               isinstance(obj, datetime.date):
                return obj.isoformat()[:10]
            return json.JSONEncoder.default(self, obj)

    class ExceptionErrorEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, dict):
                return
            return str(obj)


def datetimeToISO(obj):
    """Dipakai oleh rapidjson."""
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()[:10]
    return str(obj)[:10]


# code by angstwad
def dict_merge(dct, merge_dct):
    """Recursive dict merge.

    Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict) and
                isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def getEtag(content):
    """Hitung entity tag."""
    tag = 'W/'  # Weak eTag
    if len(content) == 0:
        return tag + '"d41d8cd98f00b204e9800998ecf8427e"'
    else:
        hashed = hashlib.md5(bytes(content, 'utf8')).hexdigest()
        return tag + '"' + hashed + '"'


def dumpAsJSON(data_in):
    """Mengubah dict JSON.

    NOTE: All date type is dumped in ISO8601 format
    """
    if json.__name__ == 'rapidjson':
        # UM_NONE = 0,
        # UM_CANONICAL = 1<<0, // 4-dashed 32 hex chars: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        # UM_HEX = 1<<1 // canonical OR 32 hex chars in a row
        if DEBUG:
            # pretty output, debug only
            data_out = json.dumps(data_in, default=datetimeToISO, uuid_mode=json.UM_CANONICAL, indent=4)
        else:
            # pure JSON
            data_out = json.dumps(data_in, datetime_mode=json.DM_ISO8601, uuid_mode=json.UM_CANONICAL) # speed 1.8xx
    elif json.__name__ == 'ujson':
            data_out = ujson.dumps(content)
    else:
        if DEBUG:
            # pretty output, debug only
            # data_out = ujson.dumps(content)
            data_out = json.dumps(content, cls=DatetimeEncoder, sort_keys=True, indent=4 * ' ')
            # data_out = json.dumps(content, ensure_ascii=False)
        else:
            # pure JSON
            # data_out = rjson.dumps(content, default=datetimeToISO) # speed 1.6xx
            # data_out = ujson.dumps(content)
            data_out = json.dumps(content, cls=DatetimeEncoder) # speed 1.8xx
            # data_out = sjson.dumps(sjson.loads(content), use_decimal=False)
            # data_out = json.dumps(content) #not work for datetime.date field

    return data_out


def isJinshi(x):
    return ('l', 'p').count(x)
