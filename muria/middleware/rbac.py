import falcon

from falcon_policy import RoleBasedPolicy
from falcon_policy.config import PolicyConfig
from falcon_policy.policy import PolicyManager


class RBAC(RoleBasedPolicy):
    # NOTE:
    # It requires jwt_checker middleware declared before itself
    # in order to work.

    # Added check_jwt if roles are passed within jwt claims
    # as an alternative if we don't want to pass X-Roles
    # inside every request header.
    def __init__(self, config_dict, check_jwt=False):
        self.config = PolicyConfig(config_dict)
        self.manager = PolicyManager(self.config)
        self.check_jwt = check_jwt

    def process_resource(self, req, resp, resource, params):
        route = req.uri_template
        if self.check_jwt and isinstance(params, dict):
            claims = params.get('jwt_claims')
            roles_header = isinstance(claims, dict) and claims.get('roles') or '@unknown'
        else:
            roles_header = req.get_header('X-Roles', default='@unknown')

        if isinstance(roles_header, str):
            provided_roles = [role.strip() for role in roles_header.split(',')]
        else:
            provided_roles = roles_header

        route_policy = self.manager.policies.get(route, {})
        method_policy = route_policy.get(req.method.upper(), [])

        has_role = self.manager.check_roles(provided_roles, method_policy)

        if not has_role:
            raise falcon.HTTPForbidden(
                description='Access to this resource has been restricted'
            )
