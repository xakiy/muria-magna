
import falcon
import rapidjson
from muria.lib.form import FormHandler
from muria.middleware.authlib import OAuth2Server
from muria.middleware.authlib.model import (
    connection,
    OAuth2Client,
    OAuth2Token
)
from muria.middleware.authlib.ponies import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from muria.middleware.authlib.grants import (
    AuthorizationCodeGrant,
    PasswordGrant,
    RefreshTokenGrant
)

dbconf = {
    'provider': 'sqlite',
    'filename': 'oauth.db',
    'create_db': True
}

#: database connection
connection.bind(**dbconf)
connection.generate_mapping(create_tables=True)

#: app initialization
app = application = falcon.API()

#: form data handler
extra_handlers = {"application/x-www-form-urlencoded": FormHandler()}
if not app.req_options.auto_parse_form_urlencoded:
    #: form data can be accessed via req.media
    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)
else:
    #: otherwise via req.params
    app.req_options.auto_parse_form_urlencoded = True


#: oauth2 stuff
oauth2_conf = {
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
}
query_client = create_query_client_func(OAuth2Client)
save_token = create_save_token_func(OAuth2Token)
authorization = OAuth2Server(
    query_client=query_client,
    save_token=save_token,
    **oauth2_conf
)

# support all grants
authorization.register_grant(grants.ImplicitGrant)
authorization.register_grant(grants.ClientCredentialsGrant)
authorization.register_grant(AuthorizationCodeGrant)
authorization.register_grant(PasswordGrant)
authorization.register_grant(RefreshTokenGrant)

# support revocation
revocation_cls = create_revocation_endpoint(OAuth2Token)
authorization.register_endpoint(revocation_cls)



# protect resource
# require_oauth = ResourceProtector()
# bearer_cls = create_bearer_token_validator(OAuth2Token)
# require_oauth.register_token_validator(bearer_cls())



class Login(object):
    """Login provider."""

    def on_get(self, req, resp, **args):
        """Here we provide user with login page."""
        print('params:', req.params)
        print('media:', req.media)
        resp.status = falcon.HTTP_OK
        resp.set_header("WWW-Authenticate", "Bearer")
        # content = {"WWW-Authenticate": "Bearer"}
        resp.content_type = "text/html"
        resp.data = open('muria/middleware/authlib/template/login.html', 'rb').read()

    def on_post(self, req, resp, **args):
        print('params:', req.params)
        print('media:', req.media)

        #: if succed we should redirect user to authorization page
        if req.media.get('password'):
            resp.status = falcon.HTTP_OK
            template = open('muria/middleware/authlib/template/authorization.html', 'r').read()
            template = template.replace('clientValue', req.media.get('client'))
            template = template.replace('usernameValue', req.media.get('username'))
            resp.content_type = 'text/html'
            resp.body = template
        else:
            resp.status = falcon.HTTP_UNAUTHORIZED
            content = {
                "content_type": req.content_type,
                "media": req.media,
                "params": req.params
            }
            # resp.content_type = "application/x-www-form-urlencoded"
            # resp.body = rapidjson.dumps(content)
            resp.media = req.media


print("================================")
print("=  Falcon Oauth2 is Running    =")
print("================================")

#: User login resource/endpoint
app.add_route("/login", Login())

#: User login resource/endpoint
# app.add_route("/logout", Logout())

#: Client authorization resource/endpoint
# app.add_route("/autorization", Oauth2Authorization())

#: Client token resource/endpoint
# app.add_route("/token", Oauth2Token())

#: Client revocation resource/endpoint
# app.add_route("/revoke", Oauth2TokenRevocation())

#: Client introspection resource/endpoint
# app.add_route("/introspec", Oauth2TokenIntrospection())

#: Other protected resouces; related with scopes
# app.add_route("/profile", Profile())
# app.add_route("/secret/api", Secret())
# app.add_route("/test", TestServer())


"""

CLIENT                   USER                    AUTHOZIATION PAGE

   <-------- open <--------#
                 user opens client app

   #-----------> redirect to auth server --------------->
                                                proceed if user has logged in
                                                otherwise log user in first

   <------------ redirect back to client <--------------#
                (with token if authorized)      user will authorize or deny
                                                the request

   #-----------> exchange token w access --------------->
                 token                           server will generate access
                                                 token and refresh token

   <------------ redirect back to client <--------------#
                 (w/ access + access token)

   #-----------> client uses access token --------------->
                 to access resource within
                 scopes
"""
