"""Testing Authentication."""

import os
import jwt
import pytest
import falcon
import pickle
import time

from falcon import testing
from pony.orm import db_session
# from urllib.parse import urlencode

if os.environ.get('MURIA_SETUP') is None:
    os.environ['MURIA_SETUP'] = os.path.join(os.path.dirname(__file__), 'test.setup.ini')

from muria.init import config
from muria.wsgi import app
from muria.libs import dumpAsJSON

@pytest.fixture
def _client():
    return testing.TestClient(app)

def _pickling(stuff, filename):
    with open(filename, 'wb') as f:
        pickle.dump(stuff, f, pickle.HIGHEST_PROTOCOL)

def _unpickling(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

class Personal(object):

    @db_session
    @pytest.mark.order5
    def get_persons(self, _client):

        access_token = _unpickling('access_token')

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        }

        resp = _client.simulate_get(
            '/persons',
            headers=headers, protocol=proto
        )

        content = resp.json.get('persons')
        assert resp.status == falcon.HTTP_OK
        assert isinstance(content, list)
        assert len(content) > 0

    @db_session
    def post_person(self, _client):
        from muria.db.model import Orang, Pengguna, Kewenangan
        from tests._data_generator import DataGenerator

        data_generator = DataGenerator()

        # generate random person
        someone = data_generator.makeOrang(sex='male')

        access_token = _unpickling('access_token')

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        }

        resp = _client.simulate_post(
            '/persons/' + someone['id'],
            body=dumpAsJSON(someone),
            headers=headers, protocol=proto
        )

        # assert 'foo' == '/persons/' + someone['id']
        assert resp.status == falcon.HTTP_201
