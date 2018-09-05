import datetime, sys, random
# from muria.init import config
from muria.db import model as Models
# import db.schema as Schemas
from pony.orm import db_session, flush, commit
from tests.data_generator import DataGenerator

exit(config.get('path', 'config_dir'))

data_generator = DataGenerator()

def pushOrang(count=20):
    count = eval(count) if isinstance(eval(count), int) else 20
    with db_session:
        for i in range(0, count):
            if random.randint(0,1) == 0:
                someone = data_generator.makeOrang(sex='male')
                person = Models.Orang(**someone)
                creds = data_generator.makePengguna(person)
                pengguna = Models.Pengguna(**creds)
            else:
                someone = data_generator.makeOrang(sex='female')
                person = Models.Orang(**someone)
                creds = data_generator.makePengguna(person)
                pengguna = Models.Pengguna(**creds)
        flush()

'''
def pushSantri(count = 20):
    count = eval(count) if isinstance(eval(count), int) else 20
    with db_session:
        for i in range(0, count):
            if random.randint(0,1) == 0:
                fulan = data_generator..makeSantri(sex='male')
                santri = Santri(**fulan)
            else:
                fulanah = data_generator..makeSantri(sex='female')
                santriwati = Santri(**fulanah)
    Models.db.commit()
'''

def timer(func):
    start = datetime.datetime.now()
    pushOrang(count)
    finish = datetime.datetime.now()


if __name__ == '__main__':
    import sys
    jenis = ('Person', 'Santri')[sys.argv.count('santri')]
    count = input("Mau buat berapa {0}?: ".format( jenis ))

    # start timer
    start = datetime.datetime.now()

    if sys.argv.count('santri'):
        pushSantri(count)
    else:
        pushOrang(count)

    finish = datetime.datetime.now()
    # finishing

    total = finish - start
    print("Took about: {0} seconds to complete {1} pushes of {2}!".format(total.total_seconds(), count, jenis))
