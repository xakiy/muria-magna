from authlib.oauth2 import (
    AuthorizationServer as OAuthorizationServer,
    OAuth2Request,
    ClientAuthentication
)

from authlib.common.security import generate_token
from authlib.common.encoding import to_unicode
from authlib.oauth2.rfc6750 import BearerToken

from .helpers import query_client, save_token

GRANT_TYPES_EXPIRES = {
    'authorization_code': 864000,
    'implicit': 3600,
    'password': 864000,
    'client_credentials': 864000
}

class OAuth2Server(OAuthorizationServer):

    def __init__(self, query_client=query_client, save_token=save_token, **config):
        super(AuthorizationServer, self).__init__(
            query_client, generate_token, save_token, **config)
        self.generate_token = generate_token
        if query_client is not None:
            self.query_client = query_client
            self.authenticate_client = ClientAuthentication(query_client)
        if save_token is not None:
            self.save_token = save_token
        '''
        'SECRET_KEY': 'secret',
        'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
        '''
        # self.config.setdefault('error_uris', app.config.get('OAUTH2_ERROR_URIS'))
        # self.generate_token = self.create_bearer_token_generator(app)

    def create_oauth2_request(self, req):
        """Resource owner will invode this request to authorize the client."""
        return OAuth2Request(req.method, req.uri, req.media, req.headers)

    def handle_response(self, status_code, payload, headers):
        if isinstance(payload, dict):
            payload = json.dumps(payload)

        # should be resp.body, resp.
        return Response(payload, status=status_code, headers=headers)

    def send_signal(self, name, *args, **kwargs):
        if name == 'after_authenticate_client':
            client_authenticated.send(self, *args, **kwargs)
        elif name == 'after_revoke_token':
            token_revoked.send(self, *args, **kwargs)

    def create_token_expires_in_generator(self, app):
        """Create a generator function for generating ``expires_in`` value.
        Developers can re-implement this method with a subclass if other means
        required. The default expires_in value is defined by ``grant_type``,
        different ``grant_type`` has different value. It can be configured
        with::

            OAUTH2_TOKEN_EXPIRES_IN = {
                'authorization_code': 864000,
                'urn:ietf:params:oauth:grant-type:jwt-bearer': 3600,
            }
        """
        expires_conf = app.config.get('OAUTH2_TOKEN_EXPIRES_IN')
        return create_token_expires_in_generator(expires_conf)

    def create_bearer_token_generator(self, app):
        """Create a generator function for generating ``token`` value. This
        method will create a Bearer Token generator with
        :class:`authlib.oauth2.rfc6750.BearerToken`. By default, it will not
        generate ``refresh_token``, which can be turn on by configuration
        ``OAUTH2_REFRESH_TOKEN_GENERATOR=True``.
        """
        conf = app.config.get('OAUTH2_ACCESS_TOKEN_GENERATOR', True)
        access_token_generator = create_token_generator(conf, 42)

        conf = app.config.get('OAUTH2_REFRESH_TOKEN_GENERATOR', False)
        refresh_token_generator = create_token_generator(conf, 48)

        expires_generator = self.create_token_expires_in_generator(app)
        return BearerToken(
            access_token_generator,
            refresh_token_generator,
            expires_generator
        )

    def validate_consent_request(self, request=None, end_user=None):
        """Validate current HTTP request for authorization page. This page
        is designed for resource owner to grant or deny the authorization::

            @app.route('/authorize', methods=['GET'])
            def authorize():
                try:
                    grant = server.validate_consent_request(end_user=current_user)
                    return render_template(
                        'authorize.html',
                        grant=grant,
                        user=current_user
                    )
                except OAuth2Error as error:
                    return render_template(
                        'error.html',
                        error=error
                    )
        """
        req = self.create_oauth2_request(request)
        req.user = end_user

        grant = self.get_authorization_grant(req)
        grant.validate_consent_request()
        if not hasattr(grant, 'prompt'):
            grant.prompt = None
        return grant


def create_token_expires_in_generator(expires_in_conf=None):
    data = {}
    data.update(GRANT_TYPES_EXPIRES)
    if expires_in_conf:
        data.update(expires_in_conf)

    def expires_in(client, grant_type):
        return data.get(grant_type, BearerToken.DEFAULT_EXPIRES_IN)

    return expires_in


def create_token_generator(token_generator_conf, length=42):
    if callable(token_generator_conf):
        return token_generator_conf

    if isinstance(token_generator_conf, str):
        return import_string(token_generator_conf)
    elif token_generator_conf is True:
        def token_generator(*args, **kwargs):
            return generate_token(length)
        return token_generator
