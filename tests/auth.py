"""Testing Authentication."""

import jwt
import pytest
import falcon
import time

from pony.orm import db_session
# from urllib.parse import urlencode

from muria.init import config
from muria.lib.misc import dumpAsJSON
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
            assert resp.json == {'WWW-Authenticate': 'Bearer'}
            assert resp.headers.get('www-authenticate') == 'Bearer'


    @pytest.mark.order2
    def post_login_and_get_tokens(self, _client):
        """Testing Authentication via POST."""

        proto = 'http'  # 'https'
        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience')
        }
        credentials = {
            "username": self.creds['username'],
            "password": self.digest_pass
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
        _pickling(self.creds, 'creds')
        _pickling(self.someone, 'someone')
        _pickling(self.digest_pass, 'digest_pass')

        # self.user is from pytest fixture within the conftest.py
        assert payload['name'] == self.user.orang.nama
        assert payload['pid'] == str(self.user.orang.id)
        assert payload['roles'] == [ x for x in self.user.kewenangan.wewenang.nama ]


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
        ## Veriy token whether it is valid or not

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

        # tamper the token
        broken_token = access_token.replace('.', '')

        payload = {
            "access_token": broken_token
        }

        resp = _client.simulate_post(
            '/auth/verify',
            body=dumpAsJSON(payload),
            headers=headers, protocol=proto
        )

        assert resp.status == falcon.HTTP_400
