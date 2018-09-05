"""muria tokenizer file."""

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

# import jwt
import hashlib
import binascii
import secrets
from init import config


class Tokenizer(object):

    def __init__(self, ecdsa=True, rsa=False):

        self.private_key = config.getbinary('security', 'private_key')
        self.public_key = config.getbinary('security', 'public_key')
        self.algorithm = config.get('security', 'algorithm')

    def hashPassword(self, text):
        """ Hash password menyerupai MySQL password() bekerja,
        select sha1(unhex(sha1('text'))) """
        hex_digested = hashlib.sha1(bytes(text, 'utf8')).hexdigest()
        hashed_bin = binascii.unhexlify(hex_digested)
        hashed = hashlib.sha1(hashed_bin).hexdigest()
        return hashed
