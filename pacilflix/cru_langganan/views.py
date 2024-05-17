from django.utils import timezone
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def kelola_langganan(request):
    username = request.COOKIES.get('username')

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
                AND t.end_date_time >= CURRENT_DATE
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
                t.nama_paket, p.harga, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran
            ORDER BY
                p.harga DESC;
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

def beli_langganan(request, nama_paket):
    with connection.cursor() as cursor:
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
            WHERE 
                p.nama = %s
            GROUP BY
                p.nama, p.harga, p.resolusi_layar;
        ''', [nama_paket])

        package = cursor.fetchone()

    return render(request, 'beli_langganan.html', {'package': package})

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        nama_paket = request.POST.get('nama_paket')
        payment_method = request.POST.get('payment_method')

        current_timestamp = timezone.now()

        start_date = current_timestamp
        end_date = start_date + timezone.timedelta(days=30)
        
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT(*) 
                FROM Transaction 
                WHERE username = %s 
                    AND end_date_time >= CURRENT_DATE
            ''', [username])
            paket_aktif_count = cursor.fetchone()[0]

            if paket_aktif_count > 0:
                cursor.execute('''
                    UPDATE Transaction 
                    SET end_date_time = %s,
                        nama_paket = %s,
                        start_date_time = %s,
                        metode_pembayaran = %s,
                        timestamp_pembayaran = %s
                    WHERE username = %s AND end_date_time >= CURRENT_DATE
                ''', [end_date.isoformat(), nama_paket, start_date.isoformat(), payment_method, current_timestamp.isoformat(), username])
            else:
                cursor.execute('''
                    INSERT INTO Transaction (username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', [username, nama_paket, start_date.isoformat(), end_date.isoformat(), payment_method, current_timestamp.isoformat()])
        
        return redirect('langganan:kelola_langganan')
