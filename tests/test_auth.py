import pytest
import falcon
import json

from falcon import testing
from pony.orm import db_session
# from urllib.parse import urlencode

from wsgi import config
from wsgi import app

@pytest.fixture
def client():
    return testing.TestClient(app)

def test_auth_get(client):
    resp = client.simulate_get('/auth')
    assert resp.status == falcon.HTTP_OK
    if config.getboolean('app', 'debug'):
        assert resp.json == {'password': 'your password', 'username': 'your username'}

@db_session
def test_auth_post(client):
    import jwt
    from muria.entity import Pengguna

    proto = 'http'  # 'https'
    headers = {"Content-Type": "application/json", "HOST": "api.krokod.net"}
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    credentials = {"username": "ahmad.yusuf", "password": "rahasiamen"}

    resp = client.simulate_post('/auth', body=json.dumps(credentials), headers=headers, protocol=proto)

    assert resp.status == falcon.HTTP_OK

    token = resp.json.get('token')

    payload = jwt.decode(
        token,
        key=config.get('security', 'public_key'),
        algorithm=config.get('security', 'algorithm'),
        issuer=config.get('security', 'issuer'),
        audience=config.get('security', 'audience'))

    user = Pengguna.get(**credentials)

    assert isinstance(user, Pengguna)
    assert payload['name'] == user.orang.nama
    assert payload['pid'] == user.orang.id.hex
    assert payload['roles'] == user.wewenang.nama

'''
def test_persons_head(client):
    response = client.simulate_head('/persons')

    assert response.status == falcon.HTTP_200 #UNAUTHORIZED
'''
