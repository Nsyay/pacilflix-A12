from django.db import connection
from django.shortcuts import render

# Create your views here.
def ulasan(request, id_tayangan):
    ulasans = []
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM ULASAN WHERE id_tayangan = '{id_tayangan}'")
        ulasans = cursor.fetchall()

        cursor.execute(
            f"SELECT judul FROM TAYANGAN WHERE id = '{id_tayangan}'")
        judul = cursor.fetchone()

    context = {
        'judul' : judul,
        'ulasans': ulasans,
    }
    response = render(request, 'ulasan.html', context)
    return response