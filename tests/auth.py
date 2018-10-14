"""Testing Authentication."""

import jwt
import pytest
import falcon
import time

from falcon import testing
from pony.orm import db_session
# from urllib.parse import urlencode

import tests._config

from muria.init import config
from muria.libs import dumpAsJSON
from tests._pickles import _pickling, _unpickling


class Auth(object):
    """Authentication Test."""

    @pytest.mark.order1
    def simple_auth_get(self, _client):
        """
        Testing Authentication via GET.

        Return simple JSON template
        that used as auth POST payload
        """
        resp = _client.simulate_get('/auth')
        assert resp.status == falcon.HTTP_OK
        if config.getboolean('app', 'debug'):
            assert resp.json == {'password': 'your password', 'username': 'your username'}

    @db_session
    @pytest.mark.order2
    def post_login_and_get_tokens(self, _client):
        """Testing Authentication via POST."""
        from muria.db.model import Orang, Pengguna, Kewenangan
        from tests._data_generator import DataGenerator

        data_generator = DataGenerator()

        # generate random person
        someone = data_generator.makeOrang(sex='male')
        # populate him
        person = Orang(**someone)
        # generate a user based on previous person
        creds = data_generator.makePengguna(person)
        # populate him
        user = Pengguna(**creds)
        # generate a wewenang
        wewenang = data_generator.makeKewenangan(person)
        # grant kewenangan
        kewenangan = Kewenangan(**wewenang)

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience')
        }
        credentials = {
            "username": creds['username'],
            "password": creds['password']
        }

        resp = _client.simulate_post(
            '/auth',
            body=dumpAsJSON(credentials),
            headers=headers, protocol=proto
        )

        assert resp.status == falcon.HTTP_OK

        # getting token
        access_token = resp.json.get('access_token')
        refresh_token = resp.json.get('refresh_token')

        payload = jwt.decode(
            access_token,
            key=config.getbinary('security', 'public_key'),
            algorithms=config.get('security', 'algorithm'),
            issuer=config.get('security', 'issuer'),
            audience=config.get('security', 'audience')
        )

        _pickling(access_token, 'access_token')
        _pickling(refresh_token, 'refresh_token')

        # user = Pengguna.get(**credentials)
        # print(user.to_dict())
        assert payload['name'] == user.orang.nama
        assert payload['pid'] == user.orang.id.hex
        assert payload['roles'] == [ x for x in user.kewenangan.wewenang.nama ]

    @pytest.mark.order3
    def auth_post_refresh_token(self, _client):

        old_access_token = _unpickling('access_token')
        old_refresh_token = _unpickling('refresh_token')

        # make sure that old tokens are few seconds earlier
        time.sleep(1)

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience')
        }
        payload = {
            "access_token": old_access_token,
            "refresh_token": old_refresh_token
        }

        resp = _client.simulate_post(
            '/auth/refresh',
            body=dumpAsJSON(payload),
            headers=headers, protocol=proto
        )

        new_access_token = resp.json.get('access_token')
        new_refresh_token = resp.json.get('refresh_token')

        assert resp.status == falcon.HTTP_OK
        assert new_access_token != old_access_token
        assert new_refresh_token != old_refresh_token

        old_acc_token_payload = jwt.decode(
            old_access_token,
            key=config.getbinary('security', 'public_key'),
            algorithms=config.get('security', 'algorithm'),
            issuer=config.get('security', 'issuer'),
            audience=config.get('security', 'audience'),
            options={'verify_exp': False}
        )

        new_acc_token_payload = jwt.decode(
            new_access_token,
            key=config.getbinary('security', 'public_key'),
            algorithms=config.get('security', 'algorithm'),
            issuer=config.get('security', 'issuer'),
            audience=config.get('security', 'audience'),
            options={'verify_exp': False}
        )

        assert old_acc_token_payload['iat'] < new_acc_token_payload['iat']
        assert old_acc_token_payload['exp'] < new_acc_token_payload['exp']

        old_ref_token_payload = jwt.decode(
            old_refresh_token,
            key=config.getbinary('security', 'public_key'),
            algorithms=config.get('security', 'algorithm'),
            issuer=config.get('security', 'issuer'),
            audience=config.get('security', 'audience'),
            options={'verify_exp': False}
        )

        new_ref_token_payload = jwt.decode(
            new_refresh_token,
            key=config.getbinary('security', 'public_key'),
            algorithms=config.get('security', 'algorithm'),
            issuer=config.get('security', 'issuer'),
            audience=config.get('security', 'audience'),
            options={'verify_exp': False}
        )

        assert old_ref_token_payload['iat'] < new_ref_token_payload['iat']
        assert old_ref_token_payload['exp'] < new_ref_token_payload['exp']


    @pytest.mark.order4
    def auth_post_verify_token(self, _client):

        access_token = _unpickling('access_token')

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience')
        }
        payload = {
            "access_token": access_token
        }

        resp = _client.simulate_post(
            '/auth/verify',
            body=dumpAsJSON(payload),
            headers=headers, protocol=proto
        )

        assert resp.status == falcon.HTTP_OK
        assert resp.json.get('access_token') == access_token
