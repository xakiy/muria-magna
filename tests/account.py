"""Testing Account Resource."""

import pytest
import falcon

from pony.orm import db_session
# from urllib.parse import urlencode

from muria.init import config
from muria.lib.misc import dumpAsJSON
from tests._pickles import _unpickling


class Account(object):

    @db_session
    @pytest.mark.order2
    def get_account(self, _client, cache):

        resource_path = '/accounts'

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
            resource_path,
            headers=headers, protocol=proto
        )

        self.content = resp.json.get('account')
        cache.set('muria/account_content', self.content)

        kewenangan = cache.get('muria/auth_user_wewenang', None)

        if kewenangan is not None:
            # within policy restriction only wewenang lower
            # than 4 is allowed to view accounts
            if kewenangan.get('wewenang') < 4:
                assert resp.status == falcon.HTTP_OK
                assert isinstance(self.content, dict)
                assert len(self.content) > 0
            else:
                assert resp.status == falcon.HTTP_FORBIDDEN

    @db_session
    def edit_account(self, _client, cache):
        cached_content = cache.get('muria/account_content', None)

        if cached_content is not None:
            old_email = cached_content.get('email').split('@')
            ori_nama = cached_content.get('nama').split(' ')
            ori_nama.reverse()
            nama = ('.').join(ori_nama)
            new_email = nama + '@' + old_email[-1:].pop()
            cached_content['email'] = new_email

            assert old_email != new_email

            resource_path = '/account'

            access_token = _unpickling('access_token')

            proto = 'http'  # 'https'
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
                headers=headers, protocol=proto
            )

            assert resp.status == falcon.HTTP_OK
            old_cached = cache.get('muria/account_content', None)
            for i in resp.json:
                if i == 'email':
                    assert resp.json[i] != old_cached[i]
                else:
                    assert resp.json[i] == old_cached[i]

    def change_account_password(self, _client):
        pass
