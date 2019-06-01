"""Fixtures."""

import os
import pytest
from random import randint
from falcon import testing

config_file = os.environ.get("MURIA_SETUP")

if config_file is None or config_file is "":
    os.environ["MURIA_SETUP"] = os.path.join(os.path.dirname(__file__), "settings.ini")

from muria.wsgi import app
from muria.init import config
from muria.db.model import Orang, Pengguna, Kewenangan
from tests._data_generator import DataGenerator
from tests._pickles import _pickling, _unpickling
from pony.orm import db_session


@pytest.fixture
def _client():
    return testing.TestClient(app)


@pytest.fixture(scope="class", autouse=True)
def _generateUser(request):
    with db_session:
        data_generator = DataGenerator()
        jinshi = "male" if randint(1, 100) % 2 == 0 else "female"
        # generate random person
        someone = data_generator.makeOrang(sex=jinshi)
        # populate him
        person = Orang(**someone)
        # generate a user based on previous person
        creds, password_string = data_generator.makePengguna(person)
        # populate him
        user = Pengguna(**creds)
        # generate a wewenang
        wewenang = data_generator.makeKewenangan(user)
        # grant kewenangan
        kewenangan = Kewenangan(**wewenang)

        user.kewenangan.wewenang.nama

        # secure switching in muria.init is still buggy
        # so let just stict to 'https' literally now
        request.cls.protocol = (
            "https"
        )  # if config.getboolean('security', 'secure') else 'http'
        request.cls.person = person
        request.cls.someone = someone
        request.cls.creds = creds
        request.cls.password_string = password_string
        request.cls.user = user
        request.cls.wewenang = wewenang
