from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            f'SELECT id_tayangan FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT WHERE username = \'{username}\' AND timestamp = \'{timestamp}\'')
        records_tayangan_favorit = cursor.fetchall()
        for i in range(len(records_tayangan_favorit)):
            cursor.execute(
                f'SELECT judul FROM TAYANGAN WHERE id = \'{records_tayangan_favorit[i][0]}\'')
            records_tayangan_favorit[i] = records_tayangan_favorit[i] + cursor.fetchone()
    context = {
            'status': 'success',
            'records_tayangan_favorit': records_tayangan_favorit,
            'time': timestamp
        }
    response = render(request, 'tayangan_favorit.html', context)
    return response

def hapus_daftar(request):
    username = request.COOKIES.get('username')
    timestamp = request.GET.get('timestamp')

    with connection.cursor() as cursor:
        cursor.execute(
            f'DELETE FROM DAFTAR_FAVORIT WHERE username = \'{username}\' AND timestamp = \'{timestamp}\'')
        
        cursor.execute(
            f'DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT WHERE username = \'{username}\' AND timestamp = \'{timestamp}\'')
    connection.commit()
    return redirect('daftar_favorit:daftar_favorit')

def hapus_tayangan_favorit(request):
    username = request.COOKIES.get('username')
    timestamp = request.GET.get('timestamp')
    id_tayangan = request.GET.get('id_tayangan')

    with connection.cursor() as cursor:
        cursor.execute(
            f'DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT WHERE username = \'{username}\' AND timestamp = \'{timestamp}\' \
                AND id_tayangan = \'{id_tayangan}\'')
    connection.commit()
    redirect_url = reverse('daftar_favorit:tayangan_favorit') + '?timestamp=' + timestamp
    return HttpResponseRedirect(redirect_url)