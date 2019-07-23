import uuid
import time
import json
import hashlib
import binascii
from os import urandom
from datetime import datetime, date
from pony.orm import (
    PrimaryKey,
    Required,
    Optional,
    Set,
    LongStr,
    composite_index,
    composite_key,
    commit,
)
from authlib.oauth2.rfc6749 import (
    ClientMixin,
    TokenMixin,
    AuthorizationCodeMixin,
)
from authlib.oidc.core import (
    AuthorizationCodeMixin as OIDCCodeMixin
)


class OAuth2ClientMixin(ClientMixin):
    client_id = PrimaryKey(str, 48, auto=True)
    client_secret = Optional(str, 120)
    issued_at = Required(
        int, nullable=False,
        default=lambda: int(time.time())
    )
    expires_at = Required(int, nullable=False, default=0)

    redirect_uri = Optional(str)
    token_endpoint_auth_method = Required(
        str, 48, default='client_secret_basic')
    grant_type = Required(LongStr, nullable=False, default='')
    response_type = Required(LongStr, nullable=False, default='')
    scope = Required(LongStr, nullable=False, default='')

    client_name = Required(str, 100)
    client_uri = Required(str)
    logo_uri = Optional(str)
    contact = Optional(str)
    tos_uri = Optional(str)
    policy_uri = Optional(str)
    jwks_uri = Optional(str)
    jwks_text = Optional(str)
    i18n_metadata = Optional(str)

    software_id = Optional(str, 36)
    software_version = Optional(str, 48)


    def __repr__(self):
        return '<Client: {}>'.format(self.client_id)

    @property
    def redirect_uris(self):
        if self.redirect_uri:
            return self.redirect_uri.splitlines()
        return []

    @redirect_uris.setter
    def redirect_uris(self, value):
        self.redirect_uri = '\n'.join(value)

    @property
    def grant_types(self):
        if self.grant_type:
            return self.grant_type.splitlines()
        return []

    @grant_types.setter
    def grant_types(self, value):
        self.grant_type = '\n'.join(value)

    @property
    def response_types(self):
        if self.response_type:
            return self.response_type.splitlines()
        return []

    @response_types.setter
    def response_types(self, value):
        self.response_type = '\n'.join(value)

    @property
    def contacts(self):
        if self.contact:
            return json.loads(self.contact)
        return []

    @contacts.setter
    def contacts(self, value):
        self.contact = json.dumps(value)

    @property
    def jwks(self):
        if self.jwks_text:
            return json.loads(self.jwks_text)
        return None

    @jwks.setter
    def jwks(self, value):
        self.jwks_text = json.dumps(value)

    @property
    def client_metadata(self):
        """Implementation for Client Metadata in OAuth 2.0 Dynamic Client
        Registration Protocol via `Section 2`_.

        .. _`Section 2`: https://tools.ietf.org/html/rfc7591#section-2
        """
        keys = [
            'redirect_uris', 'token_endpoint_auth_method', 'grant_types',
            'response_types', 'client_name', 'client_uri', 'logo_uri',
            'scope', 'contacts', 'tos_uri', 'policy_uri', 'jwks_uri', 'jwks',
        ]
        metadata = {k: getattr(self, k) for k in keys}
        if self.i18n_metadata:
            metadata.update(json.loads(self.i18n_metadata))
        return metadata

    @client_metadata.setter
    def client_metadata(self, value):
        i18n_metadata = {}
        for k in value:
            if hasattr(self, k):
                setattr(self, k, value[k])
            elif '#' in k:
                i18n_metadata[k] = value[k]

        self.i18n_metadata = json.dumps(i18n_metadata)

    @property
    def client_info(self):
        """Implementation for Client Info in OAuth 2.0 Dynamic Client
        Registration Protocol via `Section 3.2.1`_.

        .. _`Section 3.2.1`: https://tools.ietf.org/html/rfc7591#section-3.2.1
        """
        return dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            client_id_issued_at=self.issued_at,
            client_secret_expires_at=self.expires_at,
        )

    def get_client_id(self):
        return self.client_id

    def get_default_redirect_uri(self):
        if self.redirect_uris:
            return self.redirect_uris[0]

    def check_redirect_uri(self, redirect_uri):
        return redirect_uri in self.redirect_uris

    def has_client_secret(self):
        return bool(self.client_secret)

    def check_client_secret(self, client_secret):
        return self.client_secret == client_secret

    def check_token_endpoint_auth_method(self, method):
        return self.token_endpoint_auth_method == method

    def check_response_type(self, response_type):
        if self.response_type:
            return response_type in self.response_types
        return False

    def check_grant_type(self, grant_type):
        if self.grant_type:
            return grant_type in self.grant_types
        return False

    def check_requested_scopes(self, scopes):
        allowed = set(self.scope.split())
        return allowed.issuperset(set(scopes))


class OAuth2AuthorizationCodeMixin(AuthorizationCodeMixin):
    code = PrimaryKey(str, 120)
    client_id = Required(str, 48)
    redirect_uri = Required(LongStr, default='')
    response_type = Required(LongStr, default='')
    scope = Required(LongStr, default='')
    auth_time = Required(
        int, nullable=False,
        default=lambda: int(time.time())
    )

    def is_expired(self):
        return self.auth_time + 300 < time.time()

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def get_auth_time(self):
        return self.auth_time


class OAuth2TokenMixin(TokenMixin):
    client_id = PrimaryKey(str, 48)
    token_type = Required(str, 40)
    access_token = Required(str, 255, unique=True, nullable=False)
    refresh_token = Required(str, 255, index=True)
    scope = Required(LongStr, default='')
    revoked = Required(bool, default=False)
    issued_at = Required(
        int, nullable=False, default=lambda: int(time.time())
    )
    expires_in = Required(int, nullable=False, default=0)

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
        return self.issued_at + self.expires_in


class OIDCAuthorizationCodeMixin(OAuth2AuthorizationCodeMixin, OIDCCodeMixin):
    nonce = Required(str)

    def get_nonce(self):
        return self.nonce


def create_query_client_func(client_model):
    """Create an ``query_client`` function that can be used in authorization
    server.

    :param session: SQLAlchemy session
    :param client_model: Client model class
    """
    def query_client(client_id):
        return client_model.get(client_id=client_id)
    return query_client


def create_save_token_func(token_model):
    """Create an ``save_token`` function that can be used in authorization
    server.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    def save_token(token, req):
        if req.context.user:
            user_id = req.context.user.get_user_id()
        else:
            user_id = None
        client = req.context.client
        token_model(
            client_id=client.client_id,
            user_id=user_id,
            **token
        )
        commit()
    return save_token


def create_query_token_func(token_model):
    """Create an ``query_token`` function for revocation, introspection
    token endpoints.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """

    def query_token(token, token_type_hint, client):
        tokens = token_model.select(client_id=client.client_id, revoked=False)
        if token_type_hint == 'access_token':
            return tokens.filter_by(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            return tokens.filter_by(refresh_token=token).first()
        # without token_type_hint
        item = tokens.filter_by(access_token=token).first()
        if item:
            return item
        return tokens.filter_by(refresh_token=token).first()
    return query_token


def create_revocation_endpoint(token_model):
    """Create a revocation endpoint class with SQLAlchemy session
    and token model.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    from authlib.oauth2.rfc7009 import RevocationEndpoint
    query_token = create_query_token_func(token_model)

    class _RevocationEndpoint(RevocationEndpoint):
        def query_token(self, token, token_type_hint, client):
            return query_token(token, token_type_hint, client)

        def revoke_token(self, token):
            token.revoked = True
            commit()

    return _RevocationEndpoint


def create_bearer_token_validator(token_model):
    """Create an bearer token validator class with SQLAlchemy session
    and token model.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    from authlib.oauth2.rfc6750 import BearerTokenValidator

    class _BearerTokenValidator(BearerTokenValidator):
        def authenticate_token(self, token_string):
            tokens = session.query(token_model)
            return tokens.filter_by(access_token=token_string).first()

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            return token.revoked

    return _BearerTokenValidator
