"""Testing Personal Resource."""

import pytest
import falcon

from pony.orm import db_session
# from urllib.parse import urlencode

import tests._config

from muria.init import config
from muria.libs import dumpAsJSON
from tests._pickles import _unpickling


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
