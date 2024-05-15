from django.shortcuts import redirect, render
from django.db import connection

# Create your views here.
def daftar_favorit(request):
    username = request.COOKIES.get('username')
    records_daftar_favorit = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM DAFTAR_FAVORIT WHERE username = %s', [username])
        records_daftar_favorit = cursor.fetchall()

    context = {
        'status': 'success',
        'records_daftar_favorit': records_daftar_favorit,
    }
    response = render(request, 'daftar_favorit.html', context)
    return response

def tayangan_favorit(request):
    timestamp = request.GET.get('timestamp')
    username = request.COOKIES.get('username')
    records_tayangan_favorit = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT id_tayangan FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT WHERE username = %s AND timestamp = %s', [username, timestamp])
        records_tayangan_favorit = cursor.fetchall()
        for i in range(len(records_tayangan_favorit)):
            cursor.execute(
                f'SELECT judul FROM TAYANGAN WHERE id = %s' [records_tayangan_favorit[i][0]])
            records_tayangan_favorit[i] = records_tayangan_favorit[i] + cursor.fetchone()
    context = {
            'status': 'success',
            'records_tayangan_favorit': records_tayangan_favorit,
        }
    response = render(request, 'tayangan_favorit.html', context)
    return response