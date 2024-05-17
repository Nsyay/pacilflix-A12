import random
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponse

def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def episode(request, series_id, episode_number):
    episode_number = int(episode_number)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT judul FROM TAYANGAN WHERE id = '{series_id}'")
        series_title = cursor.fetchone()

        cursor.execute(f"SELECT * FROM EPISODE WHERE id_series = '{series_id}'")
        episodes = cursor.fetchall()
        episodes_with_index = [(i, *episode) for i, episode in enumerate(episodes)]

        if 0 <= episode_number < len(episodes):
            episode = episodes[episode_number]
        else:
            episode = None

    context = {
        'episodes' : episodes_with_index,
        'episode': episode,
        'series_title': series_title[0] if series_title else None,  # Ensure series_title is not None before accessing the title
    }
    return render(request, 'episode.html', context)


#@login_required
def film(request, film_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT judul, sinopsis, asal_negara FROM TAYANGAN WHERE id = '{film_id}'"
        )
        film_details = cursor.fetchone()

        if film_details:
            cursor.execute(
                f"SELECT genre FROM GENRE_TAYANGAN WHERE id_tayangan = '{film_id}'"
            )
            genres = [genre[0] for genre in cursor.fetchall()]

            cursor.execute(
                f"SELECT release_date_film, durasi_film FROM FILM WHERE id_tayangan = '{film_id}'"
            )
            film_info = cursor.fetchone()

            cursor.execute(
                f"SELECT id_sutradara FROM TAYANGAN WHERE id = '{film_id}'"
            )
            director_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            director = None
            if director_id:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{director_id}'"
                )
                director = cursor.fetchone()[0]

            cursor.execute(
                f"SELECT id_pemain FROM MEMAINKAN_TAYANGAN WHERE id_tayangan = '{film_id}'"
            )
            pemain_ids = cursor.fetchall()

            pemain_names = []
            for pemain_id in pemain_ids:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{pemain_id[0]}'"
                )
                pemain_name = cursor.fetchone()
                if pemain_name:
                    pemain_names.append(pemain_name[0])

            pemain = pemain_names if pemain_names else None

            cursor.execute(
                f"SELECT id_penulis_skenario FROM MENULIS_SKENARIO_TAYANGAN WHERE id_tayangan = '{film_id}'"
            )
            penulis_ids = cursor.fetchall()

            penulis_names = []
            for penulis_id in penulis_ids:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{penulis_id[0]}'"
                )
                penulis_name = cursor.fetchone()
                if penulis_name:
                    penulis_names.append(penulis_name[0])

            penulis = penulis_names if penulis_names else None

            film_details = {
                'judul': film_details[0],
                'sinopsis': film_details[1],
                'asal_negara': film_details[2],
                'genres': genres,
                'release_date_film': film_info[0],
                'durasi_film': film_info[1],
                'sutradara': director,
                'pemain' : pemain,
                'penulis' : penulis,
                'id_tayangan' : film_id
            }

    return render(request, 'film.html', {'film_details': film_details})

def series(request, series_id):
    episodes = []
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT judul, sinopsis, asal_negara FROM TAYANGAN WHERE id = '{series_id}'"
        )
        series_details = cursor.fetchone()

        if series_details:
            cursor.execute(
                f"SELECT genre FROM GENRE_TAYANGAN WHERE id_tayangan = '{series_id}'"
            )
            genres = [genre[0] for genre in cursor.fetchall()]


            cursor.execute(
                f"SELECT id_sutradara FROM TAYANGAN WHERE id = '{series_id}'"
            )
            director_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            director = None
            if director_id:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{director_id}'"
                )
                director = cursor.fetchone()[0]

            cursor.execute(
                f"SELECT id_pemain FROM MEMAINKAN_TAYANGAN WHERE id_tayangan = '{series_id}'"
            )
            pemain_ids = cursor.fetchall()

            pemain_names = []
            for pemain_id in pemain_ids:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{pemain_id[0]}'"
                )
                pemain_name = cursor.fetchone()
                if pemain_name:
                    pemain_names.append(pemain_name[0])

            pemain = pemain_names if pemain_names else None

            cursor.execute(
                f"SELECT id_penulis_skenario FROM MENULIS_SKENARIO_TAYANGAN WHERE id_tayangan = '{series_id}'"
            )
            penulis_ids = cursor.fetchall()

            penulis_names = []
            for penulis_id in penulis_ids:
                cursor.execute(
                    f"SELECT nama FROM CONTRIBUTORS WHERE id = '{penulis_id[0]}'"
                )
                penulis_name = cursor.fetchone()
                if penulis_name:
                    penulis_names.append(penulis_name[0])

            penulis = penulis_names if penulis_names else None

            cursor.execute(f"SELECT * FROM EPISODE WHERE id_series = '{series_id}'")
            episodes = cursor.fetchall()
            episodes_with_index = [(i, *episode) for i, episode in enumerate(episodes)]

            series_details = {
                'judul': series_details[0],
                'sinopsis': series_details[1],
                'asal_negara': series_details[2],
                'genres': genres,
                'sutradara': director,
                'pemain' : pemain,
                'penulis' : penulis,
                'id_tayangan' : series_id,
                'episodes' : episodes_with_index,
            }

    return render(request, 'series.html', {'series_details': series_details})

def tayangan(request):
    films = []
    seriess = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM FILM;')
        films = cursor.fetchall()
        for i in range(len(films)):
            cursor.execute(
                f'SELECT judul, sinopsis, url_video_trailer, release_date_trailer, id FROM TAYANGAN WHERE id = \'{films[i][0]}\'' )
            details = cursor.fetchone()
            films[i] = details + ('film',)

        cursor.execute(
            f'SELECT * FROM SERIES;')
        seriess = cursor.fetchall()
        for i in range(len(seriess)):
            cursor.execute(
                f'SELECT judul, sinopsis, url_video_trailer, release_date_trailer, id FROM TAYANGAN WHERE id = \'{seriess[i][0]}\'' )
            details_series = cursor.fetchone()
            seriess[i] = details_series + ('series',)


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

def insert_unduhan(request):
    username = request.COOKIES.get('username')
    id_tayangan = request.GET.get('id_tayangan')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO TAYANGAN_TERUNDUH VALUES (\'{id_tayangan}\', \'{username}\', \'{timestamp}\')')
        
    connection.commit()
    return JsonResponse({'status': 'success'})

def go_to_unduhan(request):
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

def open_ulasan(request, tayangan_id):
    return redirect('ulasan:ulasan', tayangan_id)