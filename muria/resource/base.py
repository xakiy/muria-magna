# Copyright 2017 Ahmad Ghulam Zakiy <ghulam (dot) zakiy (at) gmail.com>.
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

"""muria base resource class."""

from muria.init import config, CORS, connection
from muria.libs import dumpAsJSON, getEtag


class Resource(object):
    """
    Base Resource Class.

    Super class untuk class resource dalam muria-magna
    """

    def __init_subclass__(cls, config=config, connection=connection, **params):
        """Init class yang akan dijalankan otomatis oleh kelas turunannya."""
        super.__init_subclass__(**params)
        cls.config = config
        cls.connection = connection
        cls.cors = CORS(
            allow_origins_list=cls.config.get('cors', 'allow_origins_list'),
            allow_all_headers=True,
            allow_all_methods=True)

    def __resp__(self):
        self.resp.body = dumpAsJSON(self.content)
        self.resp.etag = getEtag(self.resp.body)
