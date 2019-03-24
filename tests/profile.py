"""Testing Account Resource."""

import pytest
import falcon
import hashlib

from pony.orm import db_session
# from urllib.parse import urlencode

from muria.init import config
from muria.lib.misc import dumpAsJSON
from tests._pickles import _unpickling
from tests._data_generator import DataGenerator


class Profile(object):

    @db_session
    def get_profile(self, _client, cache):

        resource_path = '/v1/profile'

        access_token = _unpickling('access_token')
        creds = _unpickling('creds')
        someone = _unpickling('someone')

        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        }

        resp = _client.simulate_get(
            resource_path,
            headers=headers, protocol=self.protocol
        )

        self.content = resp.json.get('account')
        cache.set('muria/account_content', self.content)

        assert resp.status == falcon.HTTP_OK
        assert self.content.get('email') == creds.get('email')
        assert self.content.get('username') == creds.get('username')
        assert self.content.get('profile')['id'] == someone['id']
        assert self.content.get('profile')['nama'] == someone['nama']

    @db_session
    def put_profile_picture(self, _client, cache):
        from PIL import Image
        from io import BytesIO, BufferedReader
        from tests._lib import create_multipart

        resource_path = '/v1/profile/picture'

        access_token = _unpickling('access_token')
        creds = _unpickling('creds')
        someone = _unpickling('someone')

        img = Image.new('RGB', (400, 300), color='green')
        # bytes_stream = BufferedReader()
        bytes_stream = BytesIO()
        img.save(bytes_stream, 'PNG')
        bytes_stream.seek(0)

        # Create the multipart data
        data, headers = create_multipart(
            bytes_stream.read(),
            fieldname='profile_image',
            filename='pict_test.png',
            content_type='image/png')

        # headers updated based on header requirements
        headers.update({
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        })

        resp = _client.simulate_put(
            resource_path,
            body=data,
            headers=headers, protocol=self.protocol
        )

        assert resp.status == falcon.HTTP_CREATED
        # assert resp.headers.get('location') == 'foo'
        # assert resp.json.get('success') == 'foo'

    @db_session
    def get_profile_picture(self, _client, cache):
        resource_path = '/v1/profile/picture'

        access_token = _unpickling('access_token')
        creds = _unpickling('creds')
        someone = _unpickling('someone')

        # headers updated based on header requirements
        headers = {
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        }

        resp = _client.simulate_get(
            resource_path,
            headers=headers, protocol=self.protocol
        )

        assert resp.status == falcon.HTTP_OK

    @db_session
    def edit_profile(self, _client, cache):
        cached_content = cache.get('muria/account_content', None)

        if cached_content is not None:
            # putting id in parent data
            cached_content['id'] = cached_content['profile']['id']

            # reversing user in email
            old_email = cached_content['email'].split('@')
            ori_nama = cached_content['profile']['nama'].split(' ')
            ori_nama.reverse()
            nama = ('.').join(ori_nama)
            new_email = nama + '@' + old_email[-1:].pop()

            assert cached_content['email'] != new_email

            cached_content['email'] = new_email

            # reversing username
            new_username = cached_content['username'].split('.')
            new_username.reverse()
            new_username = ('.').join(new_username)

            assert cached_content['username'] != new_username

            cached_content['username'] = new_username

            resource_path = '/v1/profile'

            access_token = _unpickling('access_token')

            # headers updated based on header requirements
            headers = {
                "Content-Type": "application/json",
                "Host": config.get('security', 'issuer'),
                "Origin": config.get('security', 'audience'),
                "Authorization": 'Bearer ' + access_token
            }

            resp = _client.simulate_patch(
                resource_path,
                body=dumpAsJSON(cached_content),
                headers=headers, protocol=self.protocol
            )

            assert resp.status == falcon.HTTP_OK

            old_cached = cache.get('muria/account_content', None)
            response = resp.json.get('account')

            assert response['email'] != old_cached['email']
            assert response['username'] != old_cached['username']

    @db_session
    def change_account_password(self, _client):

        resource_path = '/v1/profile/security'

        access_token = _unpickling('access_token')
        creds = _unpickling('creds')
        password_string = _unpickling('password_string')

        new_pass = DataGenerator().randomChar(10)

        data = {
            "old_password": password_string,
            "new_password": new_pass
        }

        # headers updated based on header requirements
        headers = {
            "Content-Type": "application/json",
            "Host": config.get('security', 'issuer'),
            "Origin": config.get('security', 'audience'),
            "Authorization": 'Bearer ' + access_token
        }

        resp = _client.simulate_patch(
            resource_path,
            body=dumpAsJSON(data),
            headers=headers, protocol=self.protocol
        )

        assert resp.status == falcon.HTTP_CREATED
