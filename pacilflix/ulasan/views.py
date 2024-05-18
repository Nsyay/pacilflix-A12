import datetime
from django.db import DatabaseError, connection
from django.shortcuts import redirect, render

def ulasan(request, id_tayangan):
    ulasans = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ULASAN WHERE id_tayangan = %s", [id_tayangan])
        ulasans = cursor.fetchall()

        cursor.execute("SELECT id, judul FROM TAYANGAN WHERE id = %s", [id_tayangan])
        judul = cursor.fetchone()

    context = {
        'judul': judul,
        'ulasans': ulasans,
        'id_tayangan': id_tayangan,
    }
    return render(request, 'ulasan.html', context)

def submit_ulasan(request, id_tayangan):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        rating = request.POST.get('rating')
        deskripsi = request.POST.get('deskripsi')
        timestamp = datetime.datetime.now()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM ULASAN WHERE id_tayangan = %s AND username = %s", [id_tayangan, username])
                ulasan_exist = cursor.fetchone()
                if ulasan_exist:
                    error = 'Anda sudah memberikan ulasan untuk tayangan ini sebelumnya.'
                    cursor.execute("SELECT * FROM ULASAN WHERE id_tayangan = %s", [id_tayangan])
                    ulasans = cursor.fetchall()
                    cursor.execute("SELECT id, judul FROM TAYANGAN WHERE id = %s", [id_tayangan])
                    judul = cursor.fetchone()
                    return render(request, 'ulasan.html', {'judul': judul, 'ulasans': ulasans, 'error': error, 'id_tayangan': id_tayangan})

                query = """
                INSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, [id_tayangan, username, timestamp, rating, deskripsi])

            return redirect(f'../tayangan/{id_tayangan}')

        except DatabaseError:
            error = 'Terjadi kesalahan, silakan coba lagi.'
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ULASAN WHERE id_tayangan = %s", [id_tayangan])
                ulasans = cursor.fetchall()
                cursor.execute("SELECT id, judul FROM TAYANGAN WHERE id = %s", [id_tayangan])
                judul = cursor.fetchone()
            return render(request, 'ulasan.html', {'judul': judul, 'ulasans': ulasans, 'error': error, 'id_tayangan': id_tayangan})

    return redirect(f'../tayangan/{id_tayangan}')
