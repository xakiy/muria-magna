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
"""muria main app, wsgi."""

import falcon
import os

from init import config
from init import connection
from init import middleware_list
# from muria import tokenizer
from muria import auth
from muria import personal
#from muria import lembaga
from muria import asrama
#from muria import stats
#from muria import downstreamer
# from muria import devel


app = application = falcon.API(middleware=middleware_list)

app.req_options.auto_parse_form_urlencoded = True

from route import static_route, resource_route

for (path, url) in static_route:
    app.add_static_route(path, url)
# sr = map(app.add_static_route, static_route)
# print(sr)

for (path, resource) in resource_route:
    app.add_route(path, resource)
