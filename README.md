# Muria-Magna
Sistem Informasi Pesantren

Merupakan microservice(API) sistem informasi pesantren yang berbasis Python.

# Instalasi
Silahkan clone reponya
- clone https://github.com/xakiy/muria-magna.git

Install package dependensinya
- pip install -r requirement-devel.txt

Siapkan file konfigurasinya yang di acu oleh env MURIA_SETUP.
1. Copy file tests/settings.ini, silahkan modifikasi sesuai kebutuhan
2. Jangan lupa buat file ssl-nya, buat yang baru bila perlu
3. Lalu letakkan di folder yang Anda mau beserta file ssl-nya
4. Kemudian export sebagai env MURIA_SETUP. Umpama Anda letakkan di \
   /home/linux_user/.config/muria.ini, maka export-nya menjadi

  ```
  $export MURIA_SETUP=/home/linux_user/config/muria.ini
  ```

Kemudian jalankan servernya dengan perintah
- gunicorn --reload muria.wsgi:app

# Kontribusi
Aplikasi masih dalam pengembangan intensif, bila Anda berminat untuk berkontribusi silahkan ajukan PR.
