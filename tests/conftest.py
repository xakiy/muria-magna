"""Fixtures."""

import os
import pytest
from falcon import testing

config_file = os.environ.get('MURIA_SETUP')

if config_file is None or config_file is '':
    os.environ['MURIA_SETUP'] = \
        os.path.join(
            os.path.dirname(__file__),
            'test.setup.ini'
    )

from muria.wsgi import app

@pytest.fixture
def _client():
    return testing.TestClient(app)
