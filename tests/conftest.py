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
from pony.orm import db_session, commit


@pytest.fixture
def client():
    return testing.TestClient(app)


@pytest.fixture(scope="class", autouse=True)
@db_session
def default_user(request):

    orang = {
        'id': '7b8bccaa-5f6f-4ac0-a469-432799c12549',
        'nik': 1455367523219750,
        'nama': 'Rijalul Ghad',
        'jinshi': 'l',
        'tempat_lahir': 'Makasar',
        'tanggal_lahir': '1983-01-28',
        'tanggal_masuk': '2019-08-12'
    }

    request.cls.protocol = ("https")

    request.cls.orang = Orang.get(id=orang['id']) \
        if Orang.exists(id=orang['id']) else Orang(**orang)

    password_string = 'supersecret'
    hashed, salt = ('0d2f943bf584cc8d2181bb6678c6a8cdd459e43b231720f4a69b735d07e50910', '56d7a4c162c754262f90f345ac67c1841c715b3c')

    pengguna = {
        'orang': request.cls.orang,
        'username': 'rijalul.ghad',
        'email': 'rijalul.ghad@gmail.com',
        'password': hashed,
        'salt': salt,
        'suspended': False
    }

    request.cls.pengguna = Pengguna.get(username=pengguna['username']) \
        if Pengguna.exists(username=pengguna['username']) else Pengguna(**pengguna)

    kewenangan = {
        'pengguna': request.cls.pengguna,
        'wewenang': 4
    }

    request.cls.kewenangan = Kewenangan.get(pengguna=kewenangan['pengguna']) \
        if Kewenangan.exists(pengguna=kewenangan['pengguna']) else Kewenangan(**kewenangan)

    # roles
    request.cls.roles = [x.nama for x in request.cls.pengguna.kewenangan.wewenang]

    request.cls.password_string = password_string
