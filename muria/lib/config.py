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
"""Config library."""

import os
from configparser import ConfigParser, ExtendedInterpolation


class Parser(ConfigParser):
    """Extending ConfigParser with some special getters."""

    def __init__(self, setup, interpolation=ExtendedInterpolation(), **kwargs):
        super(Parser, self).__init__(interpolation=interpolation, **kwargs)
        if os.path.isfile(str(os.environ.get(setup))):
            conf_file = str(os.environ.get(setup))
        else:
            raise EnvironmentError('No setup environment defined!')

        if not bool(self.read(conf_file).count(conf_file)):
            raise FileNotFoundError('File konfigurasi %s tidak ditemukan' % setup)

        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.set('path', 'base_dir', app_path)
        self.set('path', 'config_dir', os.path.dirname(os.environ[setup]))

        if self.getboolean('security', 'secure'):
            priv_key = self.get('security', 'private_key')
            pub_key = self.get('security', 'public_key')

            if os.path.isfile(priv_key) and os.path.isfile(pub_key):
                self.set('security', 'private_key', open(priv_key, 'r').read())
                self.set('security', 'public_key', open(pub_key, 'r').read())
            else:
                raise FileNotFoundError('File SSL tidak ditemukan!')

    def getlist(self, section, option, delim=' ', **kwargs):
        return self.get(section, option, **kwargs).split(delim)

    def getbinary(self, section, option, **kwargs):
        return bytes(self.get(section, option, **kwargs), 'utf8')
