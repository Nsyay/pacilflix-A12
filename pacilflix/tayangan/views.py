import random
from django.shortcuts import render
from django.db import connection

def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def episode(request):
    query = "SELECT * FROM episode;"
    episodes = execute_query(query)
    return render(request, 'episode.html', {'episodes': episodes})

def film(request):
    films = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM FILM;')
        films = cursor.fetchall()
        for i in range(len(films)):
            cursor.execute(
                f'SELECT judul FROM TAYANGAN WHERE id = \'{films[i][0]}\'' )
            films[i] = films[i] + cursor.fetchone()

    context = {
        'status': 'success',
        'films': films,
    }
    response = render(request, 'tayangan.html', context)
    return response

def series(request):
    query = "SELECT * FROM series;"
    series_list = execute_query(query)
    return render(request, 'series.html', {'series_list': series_list})

def tayangan(request):
    films = []
    seriess = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM FILM;')
        films = cursor.fetchall()
        for i in range(len(films)):
            cursor.execute(
                f'SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM TAYANGAN WHERE id = \'{films[i][0]}\'' )
            details = cursor.fetchone()
            films[i] = details

        cursor.execute(
            f'SELECT * FROM SERIES;')
        seriess = cursor.fetchall()
        for i in range(len(seriess)):
            cursor.execute(
                f'SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM TAYANGAN WHERE id = \'{seriess[i][0]}\'' )
            details_series = cursor.fetchone()
            seriess[i] = details_series


    tayangan = films + seriess

    # Shuffle and select 10 random items
    random.shuffle(tayangan)
    tayangan = tayangan[:10]

    tayangan_first_half = tayangan[:5]
    tayangan_second_half = tayangan[5:]

    context = {
        'films': films,
        'seriess' : seriess,
        'tayangan' : tayangan,
        'tayangan_first_half': tayangan_first_half,
        'tayangan_second_half': tayangan_second_half,
    }
    response = render(request, 'tayangan.html', context)
    return response

def trailer(request):
    return render(request, 'trailer.html')

def trailer_guest(request):
    return render(request, 'trailer_guest.html')