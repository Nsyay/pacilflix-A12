from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from datetime import datetime


# Create your views here.

def episode(request):
    return render(request, 'episode.html')

def film(request):
    return render(request, 'film.html')

def series(request):
    return render(request, 'series.html')

def tayangan(request):
    return render(request, 'tayangan.html')

def trailer(request):
    return render(request, 'trailer.html')

def trailer_guest(request):
    return render(request, 'trailer_guest.html')

def insert_unduhan(request):
    username = 'test'
    id_tayangan = '12345678-1234-5678-1234-567812345000'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO TAYANGAN_TERUNDUH VALUES (\'{id_tayangan}\', \'{username}\', \'{timestamp}\')')
        
    connection.commit()
    return redirect('daftar_unduhan:daftar_unduhan')

def list_favorit(request):
    username = request.COOKIES.get('username')
    id_tayangan = request.GET.get('id_tayangan')
    daftar_favorit = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM DAFTAR_FAVORIT WHERE username = \'{username}\'')
        daftar_favorit = cursor.fetchall()

    options = []
    for record in daftar_favorit:
        options.append({'value':record[0], 'text':record[2]})
    
    data = {
        'dropdown_options':options,
        'id_tayangan':id_tayangan
    }

    return JsonResponse(data)

def insert_favorit(request):
    username = request.COOKIES.get('username')
    id_tayangan = request.GET.get('id_tayangan')
    timestamp = request.GET.get('timestamp')

    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT VALUES (\'{id_tayangan}\', \'{timestamp}\', \'{username}\')')
        
    connection.commit()
    return redirect('daftar_favorit:daftar_favorit')
