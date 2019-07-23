from authlib.oauth2 import OAuth2Request

from .helpers import (
    query_client,
    save_token
)

class FalconAuthlibMiddleware():

    def __init__(self, config):
        pass

    def process_resource(self, req, resp, resource, *args, **kwargs):
        #InsecureTransportError.check(uri)
        # When using req.media we assume that FormHandler Middleware is used
        resp.context.oauth2request = server.create_oauth2_request(req, resp, resource, **kwargs)

