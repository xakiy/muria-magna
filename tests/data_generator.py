""" Populator """
""" Skrip pengisi data fiktif """

import random
import datetime
import re
import json
import uuid
import string

from muria.db.model import Jinshi

class DataGenerator(object):

    def __init__(self):
        self.today = datetime.date.today().isoformat()
        self.now = datetime.datetime.now().isoformat()
        self.next6years = str(int(self.today[:4]) + 6) + self.today[4:]
        self.femaleNames = ['Dina', 'Saufa', 'Irmawati', 'Ulfa', 'Minarni', 'Afni', 'Asfia', 'Hairiyah', 'Fitri', 'Maria', 'Munawaroh', 'Nikmah', 'Artiyah', 'Sarilah', 'Nadin', 'Ika', 'Emi', 'Erni', 'Hilda', 'Ira', 'Izzah', 'Ana', 'Nita', 'Salsabila', 'Risa', 'Saraswati', 'Titin', 'Yuliana', 'Wahyuni', 'Hafsah', 'Tiara', 'Ghea', 'Indah', 'Hayyin', 'Fathimah', "Lu'luk", 'Nufus', 'Windri', 'Erin', 'Iliana', 'Fifi', 'Vivian', 'Juli', 'Yuli', 'Sandra', 'Sofia', 'Rubi', 'Rabiah', 'Husniah', 'Halimah', 'Rusmini', 'Mirna', 'Muslimah', 'Hartati', 'Lia', 'Lutfia', 'Mia', 'Maya', 'Lily', 'Diana', 'Silfie', 'Retno', 'Susi', 'Yohana', 'Suparni', 'Zahro', 'Ramadhani', 'Munisah', 'Zuhriyah', 'Vina', 'Rahma', 'Rahmi', 'Ayu', 'Anik', 'Hani', 'Hana', 'Latifah', 'Aishah', 'Zulaikha', 'Ririn', 'Anisa', 'Dewi', 'Putri', 'Suciati', 'Puji', 'Astuti', 'Jamila', 'Laksmi', 'Bunga', 'Yuanita', 'Bilqis', 'Safitri', 'Yuliana', 'Fatmawati', 'Nova', 'Rosa', 'Sri', 'Indri', 'Sofiah', 'Sari', 'Suharti', 'Rukmini', 'Binti', 'Sulistiawati', 'Gina', 'Revina', 'Alviana', 'Widuri', 'Windi', 'Wulandari', 'Ismah', 'Rafiah', 'Sulastri', 'Hilwa', 'Ida', 'Keisha', 'Meisya', 'Maisyaroh']
        self.maleNames = ['Ahmad', 'Zairi', 'Zainur', 'Salim', 'Yanto', 'Qasim', 'Mundzir', 'Hasan', 'Husnan', 'Fanani', 'Benny', 'Afandi', 'Mukhlis', 'Ahmadi', 'Arianto', 'Suheri', 'Suparman', 'Suhaimi', 'Irwanto', 'Hamdan', 'Teguh', 'Wawan', 'Iwan', 'Herman', 'Hendra', 'Rijal', 'Fahmi', 'Rendy', 'Nurman', 'Reza', 'Anton', 'David', 'Zakaria', 'Andi', 'Yahya', 'Sukarman', 'Fatih', 'Agus', 'Heri', 'Arya', 'Hilman', 'Yosep', 'Zainul', 'Zein', 'Rahmat', 'Sutikno', 'Helmi', 'Rozik', 'Maftuh', 'Sulaiman', 'Rony', 'Indra', 'Hermawan', 'Hasyim', 'Rojabi', 'Wahyudi', 'Idham', 'Ryan', 'Fathoni', 'Sholeh', 'Purniadi', 'Husni', "Ma'arif", 'Huda', 'Burhan', 'Busyro', 'Jaka', 'Bagas', 'Arif', 'Hidayat', 'Reza', 'Muammar', 'Fery', 'Yani', 'Hendri', 'Sutrisno', 'Sukarno', 'Cecep', 'Kosasih', 'Entong', 'Ilham', 'Ishak', 'Habib', 'Surya', 'Mughni', 'Farhan', 'Hartono', 'Taufan', 'Tantowi', 'Sulhan', 'Abduh', 'Hariri', 'Fauzan', 'Lukman', 'Shiddiq', 'Enda', 'Priadi', 'Tukul', 'Saiful', 'Bima', 'Krisna', 'Bisma', 'Arya', 'Dwiki', 'Setiawan', 'Yulianto', 'Irwanto', 'Irwansyah', 'Ary', 'Aryadi', 'Hardi', 'Duta', 'Dino', 'Fadhil', 'Sutikno', 'Halim', 'Husain', 'Rifky', 'Sahid', 'Sadzhili', 'Ridwan', 'Mansyur', 'Ghozali', 'Zubair', 'Lubis', 'Muhsin', 'Tiyo', 'Edi', 'Sadewa', 'Rudy', 'Rizky', 'Hakim', 'Sukadi', 'Agung', 'Tohari', 'Arbain', 'Haekal', 'Syarif', 'Hidayat', 'Jamil', 'Fino']
        self.address = ['Semarang', 'Surabaya', 'Malang', 'Jember', 'Bali', 'Banten', 'Probolinggo', 'Purbalingga', 'Wonosobo', 'Sragen', 'Jombang', 'Mojokerto', 'Pontianak', 'Padang', 'Medan', 'Aceh', 'Palembang', 'Lampung', 'Riau', 'Bangka', 'Maluku', 'Samarinda', 'Banjarmasin', 'Makassar', 'Manado', 'NTB', 'NTT', 'Flores', 'Papua', 'Manowari', 'Salatiga', 'Solo', 'Madiun', 'Magetan', 'Trenggalek', 'Klaten', 'Nganjuk', 'Tuban', 'Bojonegoro', 'Kudus', 'Gresik', 'Lamongan', 'Pasuruan', 'Bangil', 'Banyuwangi', 'Lumajang', 'Blitar', 'Kediri', 'Situbondo', 'Bandung', 'Bogor', 'Batam', 'Halmahera']
        self.domain = ['yahoo.com', 'gmail.com', 'mail.com', 'live.com', 'mail.ru']

    def randomAddress(self):
        return self.address[random.randint(0, len(self.address) - 1)]


    """ create random date """
    def randomDate(self):
        try:
            date = datetime.date(random.randint(1980, 2009), random.randint(1, 12), random.randint(1, 31)).isoformat()
        except ValueError:
            date = self.randomDate()
        return date


    def randomName(self, sex = 'male'):
        start = 0
        if sex == 'female' or sex == 'p' or sex == 'w':
            names = self.femaleNames
        else:
            names = self.maleNames

        stop = len(names) - 1
        return str(names[random.randint(start, stop)] + ' ' + names[random.randint(start, stop)])


    def randomNIK(self):
        return random.randint(eval("1" * 16), eval("9" * 16))


    def jinshi(self, sex = 'male'):
        if sex == 'female' or sex == 'p' or sex == 'w':
            return Jinshi.get(id='p')
        else:
            return Jinshi.get(id='l')


    def randomKinship(self):
        pass


    def randomDomain(self):
        stop = len(self.domain) - 1
        return str(self.domain[random.randint(0, stop)])


    def randomChar(self, size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


    def makeOrang(self, sex='male', jsonify=False):

        person = {
            "id": str(uuid.uuid4()),
            "nik": str(self.randomNIK()),
            "nama": self.randomName(sex),
            "jinshi": self.jinshi(sex),
            "tempat_lahir": self.randomAddress(),
            "tanggal_lahir": self.randomDate(),
            # "anak_ke": self.randomKinship(),
            # "tinggal_bersama": ,
            # "pekerjaan": ,
            # "penghasilan": ,
            # "pendidikan_terahir": ,
            # "phone1": ,
            # "phone2": ,
            # "email": ,
            # "tanggal_entry": self.today,
            # "tanggal_update": self.today,
            # #"harim": ,
            # #"mahram": ,
            # #"pelajar": ,
            # #"pegawai": ,
            # #"alamat": ,
        }

        if jsonify:
            person = json.dumps(person)

        return person


    def makeSantri(self, sex='male', jsonify=False):
        """Populate random data as Santri
        """

        santri = {
            "id": str(uuid.uuid4()),
            "nik": str(self.randomNIK()),
            "nama": self.randomName(sex),
            "jenis_kelamin": self.jinshi(sex),
            "tempat_lahir": self.randomAddress(),
            "tanggal_lahir": self.randomDate(),
            "anak_ke": self.randomKinship(),
            # #"tinggal_bersama": ,
            # #"pekerjaan": ,
            # #"penghasilan": ,
            # #"pendidikan_terahir": ,
            # #"phone1": ,
            # #"phone2": ,
            # #"email": ,
            # "tanggal_entry": self.today,
            # "tanggal_update": self.today,
            # #"harim": ,
            # #"mahram": ,
            # #"pelajar": ,
            # #"pegawai": ,
            # #"alamat": ,
            "nis": str(self.randomNIK()),
            "wali": None,
            # "asuhan": ,
            # "tanggal_mulai": self.today,
            # "tanggal_akhir": self.next6years,
            # #"pengurus": ,
            # #"kepala_wilayah": ,
            # #"kepala_blok": ,
            # #"ketua_kamar": ,
            "menghuni_kamar": None
        }

        if jsonify:
            santri = json.dumps(santri)

        return santri


    def makePengguna(self, orang, jsonify=False):

        pengguna = {
            "orang": str(orang.id),
            "username": orang.nama.replace(' ', '.').lower(),
            "email": orang.nama.replace(' ', '.').lower() + '@' + self.randomDomain(),
            "password": self.randomChar(size=10),
            "suspended": 0
        }

        if jsonify:
            pengguna = json.dumps(pengguna)

        return pengguna


    def makeKewenangan(self, orang, jsonify=False):

        kewenangan = {
            "pengguna": str(orang.id),
            "wewenang": 5 if orang.jinshi.id == 'l' else 6
        }

        if jsonify:
            kewenangan = json.dumps(kewenangan)

        return kewenangan
