"""Fixtures."""

import pytest
from falcon import testing
from muria.wsgi import app

@pytest.fixture
def _client():
    return testing.TestClient(app)
