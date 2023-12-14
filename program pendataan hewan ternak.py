import mysql.connector
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

con = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'peternakan',)

def mainmenu():
    print('=== MENU ===')
    print('''
    1. Pendataan Hewan Ternak
    2. Populasi Hewan Ternak
    3. Statistik
    4. Keluar''')

def pendataan():
    print('''
    1.1 Input data
    2.1 Perbarui Data
    3.1 Hapus Data''')

def inputdata(con):
    print('>>> Pendataan Hewan Ternak <<<')
    try:
        identitas = int(input('Masukkan Nomor Data: '))
        provinsi = str(input('Provinsi: '))
        kategori = str(input('Kategori Hewan: '))
        gender = str(input('Jenis Kelamin: '))
        jumlah = int(input('Jumlah Hewan: '))
        tanggal = int(input('Masukkan Tanggal: '))
        bulan = int(input('Masukkan Bulan: '))
        tahun = int(input('Masukkan Tahun: '))
        format_tanggal = date(tahun,bulan,tanggal)
        cursor = con.cursor()
        sql = 'Insert into Nomor_Data(Identitas, Provinsi, Kategori, Gender, Jumlah, Tanggal) values (%s,%s,%s,%s,%s,%s)'
        val = (identitas,provinsi,kategori,gender,jumlah,format_tanggal)
        cursor.execute(sql,val)
        con.commit()
        print('Anda Berhasil Menginput Data')
    except ValueError:
        print('Anda Tidak Berhasil Menginput Data')

def perbaruidata(con):
    print('>>> Memperbarui Pendataan Hewan Ternak <<<')
    try:
        cursor = con.cursor()
        cekpopulasi(con)
        data = int(input('Masukkan Nomor Data:  '))
        provinsi_baru = str(input('Provinsi: '))
        kategori_baru = str(input('Kategori Hewan: '))
        gender_baru = str(input('Jenis Kelamin: '))
        jumlah_baru = int(input('Jumlah Hewan: '))
        tanggal_baru = int(input('Masukkan Tanggal: '))
        bulan_baru = int(input('Masukkan Bulan: '))
        tahun_baru = int(input('Masukkan Tahun: '))
        format_tanggal_baru = date(tahun_baru, bulan_baru, tanggal_baru)
        sql = 'Update nomor_data SET provinsi=%s, kategori=%s, gender=%s, jumlah=%s, tanggal=%s WHERE identitas=%s'
        val = (provinsi_baru, kategori_baru, gender_baru, jumlah_baru, format_tanggal_baru, data)
        cursor.execute(sql,val)
        con.commit()
        print('Anda Berhasil Memperbarui Data')
    except ValueError:
        print('Anda Gagal Memperbarui Data')

def hapusdata(con):
        cursor = con.cursor()
        cekpopulasi(con)
        data = int(input('Masukkan nomor data: '))
        konfirmasi = str(input('Apakah anda yakin menghapus data? (y/n): '))
        if konfirmasi == "y":
            sql = 'DELETE FROM nomor_data Where identitas=%s'
            val = (data,)
            cursor.execute(sql,val)
            con.commit()
        print('{} Anda Berhasil Menghapus Data'.format(cursor.rowcount))

def cekpopulasi(con):
    print('>>> Populasi Hewan Ternak <<<')
    cursor = con.cursor()
    sql = "SELECT * FROM nomor_data"
    cursor.execute(sql)
    results = cursor.fetchall()
    if cursor.rowcount < 0:
        print('Tidak Terdapat Data')
    else:
        for data in results:
            print(data)
print('')

def statistik():
    print('>>> Statistik <<<')
    cursor = con.cursor()
    sql = "SELECT monthname(tanggal), SUM(jumlah) FROM nomor_data GROUP BY MONTH(tanggal)"
    cursor.execute(sql)
    result = cursor.fetchall()

    bulan = []
    jumlah = []
    for r in result:
        print(r)
        bulan.append(str(r[0]))
        jumlah.append(int(r[1]))
      
    plt.bar(bulan,jumlah)
    plt.title('Jumlah Hewan Ternak Per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah')
    plt.show()
        
    #Data Visualisasi 2
    cursor = con.cursor()
    cursor.execute("SELECT provinsi, COUNT(provinsi) FROM nomor_data GROUP BY provinsi")
    results = cursor.fetchall()
    provinsi = []
    banyaknya = []
    for r in results:
        provinsi.append(str(r[0]))
        banyaknya.append(int(r[1]))
    print(provinsi)
    print(banyaknya)
    plt.pie(banyaknya, labels=provinsi,autopct='%0.2f%%')
    plt.title('Persentase Persebaran Provinsi')
    plt.legend(provinsi, loc='lower right', bbox_to_anchor=(1.2,0))
    plt.show()

    #data visualisasi 3
    cursor = con.cursor()
    cursor.execute('SELECT gender, COUNT(gender) FROM nomor_data GROUP BY gender')
    results = cursor.fetchall()
    gender = []
    banyak = []
    for r in results:
        gender.append(str(r[0]))
        banyak.append(int(r[1]))
    print(gender)
    print(banyak)
    plt.pie(banyak, labels=gender,autopct='%0.2f%%')
    plt.title('Persentase Jenis Kelamin Hewan Ternak')
    plt.legend(gender, loc='lower right', bbox_to_anchor=(1.2,0))
    plt.show()

    #data visualisasi 4
    cursor = con.cursor()
    cursor.execute('SELECT kategori, COUNT(kategori) FROM nomor_data GROUP BY kategori')
    results = cursor.fetchall()
    kategori = []
    banyaknyaa = []
    for r in results:
        kategori.append(str(r[0]))
        banyaknyaa.append(int(r[1]))
    print(kategori)
    print(banyaknyaa)
    plt.pie(banyaknyaa, labels=kategori,autopct='%0.2f%%')
    plt.legend(kategori, loc='lower right', bbox_to_anchor=(1.2,0))
    plt.title('Persentase Kategori Hewan Ternak')
    plt.show()

count = 0
while count < 1000:
    mainmenu()
    pilih = int(input('Pilih Menu: '))
    if pilih == 1:
        pendataan()
        pilih1 = float(input('Pilih Menu: '))
        if pilih1 == 1.1:
            inputdata(con)
        elif pilih1 == 2.1:
            perbaruidata(con)
        elif pilih1 == 3.1:
            hapusdata(con)
    elif pilih == 2:
        cekpopulasi(con)
    elif pilih == 3:
        statistik()
    elif pilih == 4:
        break

    count +=1



    