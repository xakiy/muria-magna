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

""" muria main app wrapper for uwsgi, uwsgi. """

import os

if __name__ == '__main__':

    from wsgi import app
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8000, app)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('')
        print('Shutting down the server... ')
        print('Bye!')
        httpd.shutdown()
else:
    print('Please, run this "%s" file in command line!' % __name__)
