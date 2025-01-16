import mysql.connector
import datetime
from collections import Counter
from prettytable import PrettyTable

harga_jual = {
    5: {1: 69000, 3: 68500, 5: 68000, 10: 67750},
    10: {1: 136000, 3: 135000, 5: 134000, 10: 133750},
    25: {1: 335000, 3: 334000, 5: 333000, 10: 332000}
}
harga_beli = {
    5: {1: 64000, 3: 63500, 5: 65000, 10: 62750},
    10: {1: 131000, 3: 130000, 5: 129000, 10: 128750},
    25: {1: 330000, 3: 329000, 5: 328000, 10: 327000}
}

conn = mysql.connector.connect(
    host='localhost', 
    user='root',  
    password='',  
    database='beberas',      
    port=3307                
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stok (
    barang VARCHAR(255) PRIMARY KEY,
    jumlah INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transaksi_masuk (
    id_masuk VARCHAR(255) PRIMARY KEY,
    tanggal_masuk DATE,
    barang_masuk VARCHAR(255),
    jumlah_masuk INT,
    harga_total_masuk FLOAT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transaksi_keluar (
    id_keluar VARCHAR(255) PRIMARY KEY,
    tanggal_keluar DATE,
    barang_keluar VARCHAR(255),
    jumlah_keluar INT,
    harga_total_keluar FLOAT,
    total_harga_kulak FLOAT,
    keuntungan FLOAT
)
''')

def ambil_id_masuk_terakhir():
    cursor.execute("SELECT id_masuk FROM transaksi_masuk ORDER BY id_masuk DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def buat_idmasuk(counter):
    today = datetime.datetime.now()
    date_str = today.strftime('%Y%m%d')
    masuk = f"M{date_str}{counter:02d}"
    return masuk

def token_masuk():
    today = datetime.datetime.now().strftime('%Y%m%d')    
    last_id_masuk = ambil_id_masuk_terakhir()
    
    if last_id_masuk:
        last_date_str = last_id_masuk[1:9]  
        if last_date_str == today:
            last_counter = int(last_id_masuk[9:])  
            counter = last_counter + 1
        else:
            counter = 1
    else:
        counter = 1
    
    return buat_idmasuk(counter)
id_masuk_baru = token_masuk()

def ambil_id_keluar_terakhir():
    cursor.execute("SELECT id_keluar FROM transaksi_keluar ORDER BY id_keluar DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def buat_idkeluar(counter):
    today = datetime.datetime.now()
    date_str = today.strftime('%Y%m%d')
    keluar = f"K{date_str}{counter:02d}"
    return keluar

def token_keluar():
    today = datetime.datetime.now().strftime('%Y%m%d')    
    last_id_keluar = ambil_id_keluar_terakhir()
    
    if last_id_keluar:
        last_date_str = last_id_keluar[1:9]  
        if last_date_str == today:
            last_counter = int(last_id_keluar[9:])  
            counter = last_counter + 1
        else:
            counter = 1
    else:
        counter = 1
    
    return buat_idkeluar(counter)

def simpan_transaksi_masuk(transaksim):
    cursor.execute('''
    INSERT INTO transaksi_masuk (id_masuk, tanggal_masuk, barang_masuk, jumlah_masuk, harga_total_masuk)
    VALUES (%s, %s, %s, %s, %s)
    ''', (transaksim['id_masuk'], transaksim['tanggal_masuk'], transaksim['barang_masuk'], transaksim['jumlah_masuk'], transaksim['harga_total_masuk']))
    conn.commit()

def simpan_transaksi_keluar(transaksik):
    cursor.execute('''
    INSERT INTO transaksi_keluar (id_keluar, tanggal_keluar, barang_keluar, jumlah_keluar, harga_total_keluar, total_harga_kulak, keuntungan)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (transaksik['id_keluar'], transaksik['tanggal_keluar'], transaksik['barang_keluar'], transaksik['jumlah_keluar'], transaksik['harga_total_keluar'], transaksik['total_harga_kulak'], transaksik['keuntungan']))
    conn.commit()

def tambah_stok(barang, jumlah):
    cursor.execute('''
    INSERT INTO stok (barang, jumlah) VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE jumlah = jumlah + %s
    ''', (barang, jumlah, jumlah))
    conn.commit()

def kurangi_stok(barang, jumlah):
    cursor.execute('''
    UPDATE stok SET jumlah = jumlah - %s WHERE barang = %s
    ''', (jumlah, barang))
    conn.commit()

def beli_beras(berat, jumlah):
    if berat not in harga_beli:
        print('Berat tidak valid, pilih antara 5, 10, atau 25 kg.')
        return 0

    jenis_kemasan = sorted(harga_beli[berat].keys(), key=lambda x: harga_beli[berat][x])    
    total_harga = 0
    sisa_jumlah = jumlah

    for kemasan in jenis_kemasan:
        jumlah_kemasan = sisa_jumlah // kemasan
        total_harga += jumlah_kemasan * harga_beli[berat][kemasan] * kemasan
        sisa_jumlah %= kemasan
        
        if sisa_jumlah == 0:
            break

    masuk = {
        'id_masuk': token_masuk(),  
        'tanggal_masuk': datetime.datetime.now().strftime("%Y-%m-%d"),
        'barang_masuk': f"{berat}kg",
        'jumlah_masuk': jumlah,
        'harga_total_masuk': total_harga
    }
    
    simpan_transaksi_masuk(masuk)
    tambah_stok(f"{berat}kg", jumlah) 
    return total_harga

def kulak(berat, jumlah):
    if berat not in harga_beli:
        print('Berat tidak valid, pilih antara 5, 10, atau 25 kg.')
        return 0

    jenis_kemasan = sorted(harga_beli[berat].keys(), key=lambda x: harga_beli[berat][x])    
    total_harga = 0
    sisa_jumlah = jumlah

    for kemasan in jenis_kemasan:
        jumlah_kemasan = sisa_jumlah // kemasan
        total_harga += jumlah_kemasan * harga_beli[berat][kemasan] * kemasan
        sisa_jumlah %= kemasan
        
        if sisa_jumlah == 0:
            break
    return total_harga

def jual_beras(berat, jumlah):
    if berat not in harga_jual:
        print('Berat tidak valid, pilih antara 5, 10, atau 25 kg.')
        return 0

    jenis_kemasan = sorted(harga_jual[berat].keys(), key=lambda x: harga_jual[berat][x])   
    total_harga = 0
    sisa_jumlah = jumlah

    for kemasan in jenis_kemasan:
        jumlah_kemasan = sisa_jumlah // kemasan
        total_harga += jumlah_kemasan * harga_jual[berat][kemasan] * kemasan
        sisa_jumlah %= kemasan

        if sisa_jumlah == 0:
            break
            
    total_harga_kulak = kulak(berat, jumlah)
    keuntungan = total_harga - total_harga_kulak

    keluar = {
        'id_keluar': token_keluar(),  
        'tanggal_keluar': datetime.datetime.now().strftime("%Y-%m-%d"),
        'barang_keluar': f"{berat}kg",
        'jumlah_keluar': jumlah,
        'harga_total_keluar': total_harga,
        'total_harga_kulak': total_harga_kulak,
        'keuntungan': keuntungan
    }
    
    simpan_transaksi_keluar(keluar)
    kurangi_stok(f"{berat}kg", jumlah) 
    return total_harga

def batal_keluar(id_keluar, keterangan):
    cursor.execute("SELECT barang_keluar, jumlah_keluar FROM transaksi_keluar WHERE id_keluar = %s", (id_keluar,))
    result = cursor.fetchone()

    if result:
        barang, jumlah = result
        cursor.execute("SELECT * FROM batal_keluar WHERE id_keluar = %s", (id_keluar,))
        if cursor.fetchone():
            print("Transaksi sudah dibatalkan sebelumnya.")
            return
        
        # Update the stock
        cursor.execute("UPDATE stok SET jumlah = jumlah + %s WHERE barang = %s", (jumlah, barang))
        
        # Get the current date
        tanggal_sekarang = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO batal_keluar (id_keluar, tanggal_batal, keterangan) VALUES (%s, %s, %s)",
                       (id_keluar, tanggal_sekarang, keterangan))
        
        # Update the transaksi_keluar table instead of deleting
        cursor.execute("""
            UPDATE transaksi_keluar 
            SET jumlah_keluar = 0, 
                harga_total_keluar = 0, 
                total_harga_kulak = 0, 
                keuntungan = 0 
            WHERE id_keluar = %s
        """, (id_keluar,))
        
        conn.commit()
        print("Order berhasil dibatalkan.")
    else:
        print("ID penjualan tidak ditemukan.")

def idcari_penjualan(id_keluar):
    cursor.execute("SELECT * FROM transaksi_keluar WHERE id_keluar = %s", (id_keluar,))
    result = cursor.fetchone()

    if result:
        table = PrettyTable()
        table.field_names = ["id_keluar", "tanggal_keluar", "barang_keluar", "jumlah_keluar", "harga_total_keluar", "total_harga_kulak", "keuntungan"]
        table.add_row(result)
        print(table)
    else:
        print("ID transaksi tidak ditemukan.")

def idcari_penjualan(id_keluar):
    cursor.execute("SELECT * FROM transaksi_keluar WHERE id_keluar = %s", (id_keluar,))
    result = cursor.fetchone()

    if result:
        table = PrettyTable()
        table.field_names = ["id_keluar", "tanggal_keluar", "barang_keluar", "jumlah_keluar", "harga_total_keluar","total_harga_kulak","keuntungan"]
        table.add_row(result)
        print(table)
    else:
        print("ID transaksi tidak ditemukan.")

def tglcari_penjualan(tanggal_keluar):
    cursor.execute("SELECT * FROM transaksi_keluar WHERE tanggal_keluar = %s", (tanggal_keluar,))
    result = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["id_keluar", "tanggal_keluar", "barang_keluar", "jumlah_keluar", "harga_total_keluar","total_harga_kulak","keuntungan"]

    if result:
        for row in result:
            table.add_row(row)
        print(table)
    else:
        print("Tanggal tidak ditemukan.")

def terbanyak():
    cursor.execute('SELECT barang_keluar, SUM(jumlah_keluar), SUM(harga_total_keluar) FROM transaksi_keluar GROUP BY barang_keluar')
    rows = cursor.fetchall()    
    kemasan_count = Counter()
    total_penjualan = 0
    
    for row in rows:
        barang = row[0]
        jumlah = row[1]
        harga_total = row[2]
        
        kemasan_count[barang] += jumlah
        total_penjualan += harga_total
    
    print("Rekap Penjualan:")
    table = PrettyTable()
    table.field_names = ["Barang", "Jumlah Kemasan", "Total Penjualan"]
    
    for kemasan, jumlah in kemasan_count.items():
        table.add_row([kemasan, jumlah, total_penjualan])
    
    print(table)

def tampilkan_stok():
    cursor.execute('SELECT * FROM stok')
    rows = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["Barang", "Jumlah"]
    for row in rows:
        table.add_row(row)
    print(table)

def tampilkan_menu():
    print("Menu Aplikasi Uas:")
    print("1. Melayani Penjualan")
    print("2. Menambah Stok")
    print("3. Membatalkan Penjualan")
    print("4. Menampilkan penjualan berdasarkan ID") 
    print("5. Menampilkan penjualan berdasarkan TANGGAL")
    print("6. Menampilkan Banyak Penjualan") 
    print("7. Menampilkan Rekap Penjualan")
    print("8. Kemasan paling banyak terjual")
    print("9. Menampilkan transaksi masuk")
    print("10. Menampilkan stok")
    print("11. Menampilkan transaksi yang dibatalkan")
    print("12. Keluar Aplikasi")

while True:
    tampilkan_menu()
    pilihan = input("Pilih menu: ")
    if pilihan == '1':
        print('[ stok tersedia ]')
        tampilkan_stok() 
        berat = int(input('Masukkan jenis kemasan (5/10/25): '))
        jumlah = int(input('Masukkan banyak (kg): '))
        total_harga = float(jual_beras(berat, jumlah))
        print(f'Total penjualan: Rp {total_harga:.2f}')

    elif pilihan == '2':
        berat = int(input('Masukkan jenis kemasan (5/10/25): '))
        jumlah = int(input('Masukkan banyak (kg): '))
        total_harga = float(beli_beras(berat, jumlah))
        print(f'Total belanja: Rp {total_harga:.2f}')

    elif pilihan == '3':
        cursor.execute('SELECT id_keluar, tanggal_keluar, barang_keluar, jumlah_keluar, total_harga_kulak FROM transaksi_keluar')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID Keluar", "Tanggal Keluar", "Barang Keluar", "Jumlah Keluar", "Harga Total Keluar"]
    
        for row in rows:
            table.add_row(row)    
        print("TRANSAKSI YANG INGIN DIBATALKAN:")
        print(table) 

        id_keluar = input("Masukkan ID transaksi yang ingin dibatalkan: ")
        keterangan = input('Masukkan alasan pembatalan order: ')    
        batal_keluar(id_keluar, keterangan)

        cursor.execute('SELECT * FROM batal_keluar')
        batal_rows = cursor.fetchall()
    
        batal_table = PrettyTable()
        batal_table.field_names = ["id_keluar", "Tanggal Pembatalan", "Keterangan (alasan)"]    
        for batal_row in batal_rows:
            batal_table.add_row(batal_row)

        print("\nTRANSAKSI YANG DI BATALKAN:")
        print(batal_table)

    elif pilihan == '4':
        cariid = input("Masukkan ID penjualan yang ingin ditampilkan: ")      
        idcari_penjualan(cariid)

    elif pilihan == '5':
        caritgl = input("Masukkan tanggal penjualan yang ingin ditampilkan (ex= 2024-12-27): ")      
        tglcari_penjualan(caritgl)

    elif pilihan == '6':
        print('BANYAK PENJUALAN:')
        cursor.execute('''
        SELECT 
            tanggal_keluar, 
            SUM(jumlah_keluar * (barang_keluar = '5kg')) AS "5Kg", 
            SUM(jumlah_keluar * (barang_keluar = '10kg')) AS "10Kg", 
            SUM(jumlah_keluar * (barang_keluar = '25kg')) AS "25Kg" 
        FROM 
            transaksi_keluar 
        GROUP BY 
            tanggal_keluar 
        ORDER BY 
            tanggal_keluar
''')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["tanggal_keluar", "5Kg", "10Kg", "25Kg"]
        for row in rows:
            table.add_row(row)
        print(table)
        print('')
        print('TAMPILAN TRANSAKSI PENJUALAN: ')
        cursor.execute('SELECT id_keluar, tanggal_keluar, barang_keluar, jumlah_keluar, total_harga_kulak FROM transaksi_keluar')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["id_keluar", "tanggal_keluar", "barang_keluar", "jumlah_keluar", "harga_total_keluar"]
        for row in rows:
            table.add_row(row)
        print(table) 

    elif pilihan == '7':
        print('REKAP PENJUALAN:')
        cursor.execute('''
            SELECT 
                tanggal_keluar,
                barang_keluar,
                SUM(jumlah_keluar) AS total_jumlah_keluar,
                SUM(harga_total_keluar) AS total_harga_keluar,
                SUM(total_harga_kulak) AS total_harga_kulak,
                SUM(keuntungan) AS total_keuntungan
            FROM 
                transaksi_keluar
            GROUP BY 
                tanggal_keluar, barang_keluar
            ORDER BY 
                tanggal_keluar, barang_keluar;
''')
        rows = cursor.fetchall()
        rekap_data = {}
    
        for row in rows:
            tanggal, barang, total_jumlah, total_harga, total_modal, total_keuntungan = row
            if tanggal not in rekap_data:
                rekap_data[tanggal] = {
                    "5Kg": 0,
                    "10Kg": 0,
                    "25Kg": 0,
                    "Total Penjualan": 0,
                    "Total Modal": 0,
                    "Keuntungan": 0
            }        
            if barang == '5kg':
                rekap_data[tanggal]["5Kg"] += total_harga
            elif barang == '10kg':
                rekap_data[tanggal]["10Kg"] += total_harga
            elif barang == '25kg':
                rekap_data[tanggal]["25Kg"] += total_harga            
            rekap_data[tanggal]["Total Penjualan"] += total_harga
            rekap_data[tanggal]["Total Modal"] += total_modal
            rekap_data[tanggal]["Keuntungan"] += total_keuntungan

        table = PrettyTable()
        table.field_names = ["Tanggal Keluar", "5Kg", "10Kg", "25Kg", "Total Penjualan", "Total Modal", "Keuntungan"]

    # Menambahkan data ke tabel
        for tanggal, data in rekap_data.items():
            table.add_row([tanggal, data["5Kg"], data["10Kg"], data["25Kg"], data["Total Penjualan"], data["Total Modal"], data["Keuntungan"]])

        print(table)

        print('')
        print('TAMPILAN SELURUH TRANSAKSI PENJUALAN & KEUNTUNGAN: ')
        cursor.execute('SELECT*FROM transaksi_keluar')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["id_keluar", "tanggal_keluar", "barang_keluar", "jumlah_keluar", "harga_total_keluar", "total_harga_kulak", "keuntungan"]
        for row in rows:
            table.add_row(row)
        print(table)        
            
    elif pilihan == '8':
        terbanyak()

    elif pilihan == '9':
        cursor.execute('SELECT * FROM transaksi_masuk')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID Masuk", "Tanggal Masuk", "Barang Masuk", "Jumlah Masuk", "Harga Total Masuk"]
        for row in rows:
            table.add_row(row)
        print(table)              
    elif pilihan == '10':
        cursor.execute('SELECT * FROM stok')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["barang","jumlah"]
        for row in rows:
            table.add_row(row)
        print(table)
    elif pilihan == '11':
        cursor.execute('SELECT * FROM batal_keluar')
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["id_keluar","tanggal_batal","keterangan"]
        for row in rows:
            table.add_row(row)
        print(table)
    elif pilihan == '12':
        print("Semoga Nilai A, amin")
        break
    else:
        print("Pilihan tidak valid.")