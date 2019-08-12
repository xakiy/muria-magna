"""Testing Personal Resource."""

import pytest
import falcon

from pony.orm import db_session

# from urllib.parse import urlencode

from muria.init import config
from muria.lib.misc import dumpAsJSON
from tests._pickles import _unpickling


class Personal(object):
    @db_session
    def get_persons(self, client, request):

        access_token = request.config.cache.get("access_token", None)

        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get("security", "issuer"),
            "Origin": config.get("security", "audience"),
            "Authorization": "Bearer " + access_token,
        }

        resp = client.simulate_get(
            "/v1/orang", headers=headers, protocol=self.protocol
        )

        content = resp.json.get("persons")
        assert resp.status == falcon.HTTP_OK
        assert isinstance(content, list)
        assert len(content) > 0

    @db_session
    def post_person(self, client, request):
        from muria.db.model import Orang, Pengguna, Kewenangan
        from tests._data_generator import DataGenerator

        data_generator = DataGenerator()

        # generate random person
        someone = data_generator.makeOrang(sex="male")
        request.config.cache.set("posted_person", dumpAsJSON(someone))

        access_token = request.config.cache.get("access_token", None)

        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get("security", "issuer"),
            "Origin": config.get("security", "audience"),
            "Authorization": "Bearer " + access_token,
        }

        resp = client.simulate_post(
            "/v1/orang/" + someone["id"],
            body=dumpAsJSON(someone),
            headers=headers,
            protocol=self.protocol,
        )

        assert resp.status == falcon.HTTP_201

    @db_session
    def search_person(self, client, request):

        import json
        from urllib.parse import urlencode

        someone = json.loads(request.config.cache.get("posted_person", "{}"))

        access_token = request.config.cache.get("access_token", None)

        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get("security", "issuer"),
            "Origin": config.get("security", "audience"),
            "Authorization": "Bearer " + access_token,
        }

        resp = client.simulate_get(
            path="/v1/orang",
            params={"search": someone.get("nama")},
            headers=headers,
            protocol=self.protocol,
        )

        assert resp.status == falcon.HTTP_200
        assert resp.json.get("count") == 1
        assert resp.json.get("persons")[0]["nik"] == someone.get("nik")
        assert resp.json.get("persons")[0]["tanggal_lahir"] == someone.get(
            "tanggal_lahir"
        )
