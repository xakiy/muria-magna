"""Testing Authentication."""

import os
import jwt
import json
import pytest
import falcon
import pickle
import time

from falcon import testing
from pony.orm import db_session
# from urllib.parse import urlencode

if os.environ.get('MURIA_SETUP') is None:
    os.environ['MURIA_SETUP'] = os.path.join(os.path.dirname(__file__), 'test_setup.ini')

from muria.init import config
from muria.wsgi import app

@pytest.fixture
def client():
    return testing.TestClient(app)

def pickling(stuff, filename):
    with open(filename, 'wb') as f:
        pickle.dump(stuff, f, pickle.HIGHEST_PROTOCOL)

def unpickling(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


class TestAuth(object):
    """Authentication Test."""

    @pytest.mark.order1
    def test_simple_auth_get(self, client):
        """
        Testing Authentication via GET.

        Return simple JSON template
        that used as auth POST payload
        """
        resp = client.simulate_get('/auth')
        assert resp.status == falcon.HTTP_OK
        if config.getboolean('app', 'debug'):
            assert resp.json == {'password': 'your password', 'username': 'your username'}

    @db_session
    @pytest.mark.order2
    def test_auth_post_login_and_get_tokens(self, client):
        """Testing Authentication via POST."""
        from muria.db.model import Orang, Pengguna, Kewenangan
        from tests.data_generator import DataGenerator

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

        resp = client.simulate_post(
            '/auth',
            body=json.dumps(credentials),
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

        pickling(access_token, 'access_token')
        pickling(refresh_token, 'refresh_token')

        # user = Pengguna.get(**credentials)
        # print(user.to_dict())
        assert payload['name'] == user.orang.nama
        assert payload['pid'] == user.orang.id.hex
        assert payload['roles'] == [ x for x in user.kewenangan.wewenang.nama ]

    @pytest.mark.order3
    def test_auth_post_verify_token(self, client):

        access_token = unpickling('access_token')

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

        resp = client.simulate_post(
            '/auth/verify',
            body=json.dumps(payload),
            headers=headers, protocol=proto
        )

        assert resp.status == falcon.HTTP_OK
        assert resp.json.get('access_token') == access_token

        random_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJyb2xlcyI6InNhbnRyaXdhbiIsImF1ZCI6ImFwcC5naXJpbGFicy5jb20iLCJleHAiOjE1MzcyODg1NTMsImlhdCI6MTUzNzI4ODI1MywibmFtZSI6IkFobWFkIFl1c3VmIiwicGlkIjoiMTI3NjhiMmQzZDdjNDQxN2JlNThlOTk2NmM5MGZkZDYiLCJpc3MiOiJhcGkuZ2lyaWxhYnMuY29tIn0.pnFKa3oeQLANdfoj8l6hp2iK4C5Oo3TiBHofE-DBU_Q8ssZfBng3fOouHDomAW1-ZG8vxJCxqhEFtFr6hJ-W0g"



    @pytest.mark.order4
    def test_auth_post_refresh_token(self, client):

        import time

        old_access_token = unpickling('access_token')
        old_refresh_token = unpickling('refresh_token')

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

        resp = client.simulate_post(
            '/auth/refresh',
            body=json.dumps(payload),
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
