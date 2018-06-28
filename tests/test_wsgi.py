import falcon
import pytest
import json
from urllib.parse import urlencode
from falcon import testing
from pony.orm import db_session

from wsgi import config
from wsgi import app

@pytest.fixture
def client():
    return falcon.testing.TestClient(app)

def test_auth_get(client):
    response = client.simulate_get('/auth')
    assert response.content == b'{\n    "password": "your password",\n    "username": "your username"\n}'
    assert response.status == falcon.HTTP_OK

@db_session
def test_auth_post(client):
    import jwt
    from muria.entities import User
    post_data = {"username": "cecephaekal", "password": "rahasia menx"}
    body = bytes(json.dumps(post_data), 'utf-8')
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = {"Content-Type": "application/json", "HOST": "api.krokod.net"}
    response = client.simulate_post('/auth', body=body, headers=headers)

    assert response.status == falcon.HTTP_OK
    assert isinstance(response.content, bytes)
    token = json.loads(response.content).get('token')

    payload = jwt.decode(
        token,
        key=config.sec('public_key'),
        algorithm=config.sec('algorithm'))

    user = User.get(**post_data)

    assert isinstance(user, User)
    assert payload['name'] == user.pid.nama
    assert payload['pid'] == user.pid.id
    assert payload['roles'] == 'admin'


def test_persons_head(client):
    response = client.simulate_head('/persons')

    assert response.status == falcon.HTTP_200 #UNAUTHORIZED
