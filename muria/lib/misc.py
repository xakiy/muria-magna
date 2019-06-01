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
import hashlib

from muria.init import config, DEBUG


try:
    import rapidjson as json
except ImportError:
    import json

    class ConvertionEncoder(json.JSONEncoder):
        def default(self, obj):
            """Mengubah datetime sebagai string biasa."""
            if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
                return obj.isoformat()[:10]

            """Mengubah bytes menjadi string biasa."""
            if isinstance(obj, bytes):
                return obj.decode()

            """Abaikan bila sebuah dict."""
            if isinstance(obj, dict):
                return

            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError:
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
        if (
            k in dct
            and isinstance(dct[k], dict)
            and isinstance(merge_dct[k], collections.Mapping)
        ):
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
    tag = "W/"  # Weak eTag
    if len(content) == 0:
        return tag + '"d41d8cd98f00b204e9800998ecf8427e"'
    else:
        hashed = hashlib.md5(bytes(content, "utf8")).hexdigest()
        return tag + '"' + hashed + '"'


def dumpAsJSON(source):
    """Mengubah dict JSON.

    NOTE: All date type is dumped in ISO8601 format
    """
    if json.__name__ == "rapidjson":
        # UM_NONE = 0,
        # UM_CANONICAL = 1<<0, // 4-dashed 32 hex chars: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        # UM_HEX = 1<<1 // canonical OR 32 hex chars in a row
        if DEBUG:
            # pretty output, debug only
            output = json.dumps(
                source, default=datetimeToISO, uuid_mode=json.UM_CANONICAL, indent=4
            )
        else:
            # pure JSON
            output = json.dumps(
                source, datetime_mode=json.DM_ISO8601, uuid_mode=json.UM_CANONICAL
            )  # speed 1.8xx
    else:
        if DEBUG:
            # pretty output, debug only
            # output = ujson.dumps(source)
            output = json.dumps(
                source, cls=ConvertionEncoder, sort_keys=True, indent=4 * " "
            )
            # output = json.dumps(source, ensure_ascii=False)
        else:
            # pure JSON
            # output = rjson.dumps(source, default=datetimeToISO) # speed 1.6xx
            # output = ujson.dumps(source)
            output = json.dumps(source, cls=ConvertionEncoder)  # speed 1.8xx
            # output = sjson.dumps(sjson.loads(source), use_decimal=False)
            # output = json.dumps(source) #not work for datetime.date field

    return output


def isJinshi(x):
    return ("l", "p").count(x)
