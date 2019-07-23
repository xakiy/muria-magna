
from pony.orm import (
    PrimaryKey,
    Required,
    Optional,
    Set,
    LongStr,
    composite_index,
    composite_key,
    commit
)
from .ponies import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OIDCAuthorizationCodeMixin,
    OAuth2TokenMixin
)

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, 60)
    client = Set("OAuth2Client")
    authorization_code = Set("OAuth2AuthorizationCode")
    token = Set("OAuth2Token")

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return self.password == password


class OAuth2Client(db.Entity, OAuth2ClientMixin):
    id = PrimaryKey(int, auto=True)
    user_id = Required(User, cascade_delete=True)


class OAuth2Token(db.Entity, OAuth2TokenMixin):
    id = PrimaryKey(int, auto=True)
    user_id = Required(User)

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()


class OAuth2AuthorizationCode(db.Entity, AuthorizationCodeMixin):
    id = PrimaryKey(int, auto=True)
    user_id = Required(User, cascade_delete=True)


connection.generate_mapping(create_tables=True)
