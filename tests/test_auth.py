import pytest
import falcon
import json
import os

from falcon import testing
from pony.orm import db_session
# from urllib.parse import urlencode

os.environ['MURIA_SETUP'] = os.path.join(os.path.dirname(__file__), 'test_setup.ini')

from muria.init import config
from muria.wsgi import app


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
    from muria.db.model import Orang, Pengguna
    from tests.data_generator import DataGenerator

    data_generator = DataGenerator()

    someone = data_generator.makeOrang(sex='male')
    person = Orang(**someone)
    creds = data_generator.makePengguna(person)
    user = Pengguna(**creds)

    proto = 'http'  # 'https'
    headers = {
        "Content-Type": "application/json",
        "HOST": config.get('security', 'issuer'),
        "Origin": config.get('security', 'audience')}
    credentials = {"username": creds['username'], "password": creds['password']}

    resp = client.simulate_post('/auth', body=json.dumps(credentials), headers=headers, protocol=proto)

    assert resp.status == falcon.HTTP_OK

    token = resp.json.get('token')

    payload = jwt.decode(
        token,
        key=config.getbinary('security', 'public_key'),
        algorithm=config.get('security', 'algorithm'),
        issuer=config.get('security', 'issuer'),
        audience=config.get('security', 'audience'))

    # user = Pengguna.get(**credentials)
    # print(user.to_dict())
    assert payload['name'] == user.orang.nama
    assert payload['pid'] == user.orang.id.hex
    assert payload['roles'] == user.wewenang.nama


'''
def test_persons_head(client):
    response = client.simulate_head('/persons')

    assert response.status == falcon.HTTP_200 #UNAUTHORIZED
'''
