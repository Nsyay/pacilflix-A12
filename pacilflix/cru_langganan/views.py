from django.shortcuts import render
from django.db import connection

def kelola_langganan(request):
    username = request.COOKIES.get('username')
    # username = 'chikawaii'

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                t.nama_paket,
                p.harga,
                p.resolusi_layar,
                string_agg(d.dukungan_perangkat, ', ') AS dukungan_perangkat,
                t.start_date_time,
                t.end_date_time
            FROM 
                TRANSACTION t
            JOIN 
                PAKET p ON t.nama_paket = p.nama
            LEFT JOIN 
                DUKUNGAN_PERANGKAT d ON t.nama_paket = d.nama_paket
            WHERE 
                t.username = %s
                AND t.timestamp_pembayaran = (
                    SELECT MAX(timestamp_pembayaran) 
                    FROM TRANSACTION 
                    WHERE username = t.username
                )
            GROUP BY 
                t.nama_paket, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time;
        ''', [username])

        active_subscriptions = []
        for row in cursor.fetchall():
            active_subscriptions.append({
                'nama_paket': row[0],
                'harga': row[1],
                'resolusi_layar': row[2],
                'dukungan_perangkat': row[3],
                'start_date_time': row[4],
                'end_date_time': row[5]
            })

        cursor.execute('''
            SELECT 
                p.nama,
                p.harga,
                p.resolusi_layar,
                string_agg(d.dukungan_perangkat, ', ') AS dukungan_perangkat
            FROM 
                PAKET p
            LEFT JOIN 
                DUKUNGAN_PERANGKAT d ON p.nama = d.nama_paket
            GROUP BY 
                p.nama, p.harga, p.resolusi_layar;
        ''')

        all_packages = []
        for row in cursor.fetchall():
            all_packages.append({
                'nama': row[0],
                'harga': row[1],
                'resolusi_layar': row[2],
                'dukungan_perangkat':row[3]
            })

        cursor.execute('''
            SELECT 
                t.nama_paket,
                p.harga,
                t.start_date_time,
                t.end_date_time,
                t.metode_pembayaran,
                TO_CHAR(t.timestamp_pembayaran, 'YYYY-MM-DD') AS tanggal_pembayaran
            FROM 
                TRANSACTION t
            JOIN 
                PAKET p ON t.nama_paket = p.nama
            WHERE 
                t.username = %s
            GROUP BY 
                t.nama_paket, p.harga, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran;
        ''', [username])

        all_transactions = []
        for row in cursor.fetchall():
            all_transactions.append({
                'nama': row[0],
                'harga': row[1],
                'start_date_time': row[2],
                'end_date_time': row[3],
                'metode_pembayaran': row[4],
                'tanggal_pembayaran': row[5]
            })
    
    return render(request, 'kelola_langganan.html', {'active_subscriptions': active_subscriptions, 'all_packages': all_packages, 'all_transactions': all_transactions})

def beli_langganan(request):
    return render(request, 'beli_langganan.html')