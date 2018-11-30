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

"""
Handle Muria's logging session
"""

import logging

class Logger(object):

    def __init__(self, config):
        self.config = config

    def getLogger(self):
        logger = logging.getLogger(self.config.get('app', 'logger_name'))
        logger.setLevel(self.config.getint('app', 'logger_level'))
        logger.propogate = False
        if not logger.handlers:
            handler = logging.StreamHandler()
            logger.addHandler(handler)
        return logger
