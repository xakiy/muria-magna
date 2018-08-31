
import datetime
import uuid
from random import Random
import db.model as Models
# import db.schema as Schemas
from pony.orm import db_session

"""Insert data into database"""
def saveEntity(entity, data):
    try:
        ent = Models.__getattribute__(entity)
    except AttributeError:
        raise AttributeError

    newEntity = ent(**data)
    return newEntity



laki = {'id': 'l', 'nama': 'Laki-laki', 'kecil': 'Putra', 'formal': 'Pria'}
perempuan = {'id': 'p', 'nama': 'Perempuan', 'kecil': 'Putri', 'formal': 'Wanita'}


with db_session:
    l = saveEntity('Jinshi', laki)
    p = saveEntity('Jinshi', perempuan)

    orang = {
        'id': uuid.uuid4(),
        'nama': 'Ahmad Hasyim',
        'nik': str(Random().random())[2:],
        'jinshi': l,
        'tempat_lahir': 'Mataram',
        'tanggal_lahir': datetime.date.today() - datetime.timedelta(days=20*365)
    }

    foo = saveEntity('Orang', orang)

    Models.db.commit()
