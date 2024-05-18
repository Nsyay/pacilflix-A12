from django.urls import path
from .views import *

app_name = 'tayangan'

urlpatterns = [
    path('series/episode/<series_id>/<episode_number>/', episode, name='episode'),
    path('film/<film_id>/', film, name='film'),
    path('series/<series_id>/', series, name='series'),
    path('', tayangan, name='tayangan'),
    path('trailer/', trailer, name='trailer'),
    path('insert_unduhan/', insert_unduhan, name='insert_unduhan'),
    path('list_favorit/', list_favorit, name='list_favorit'),
    path('insert_favorit/', insert_favorit, name='insert_favorit'),
    path('go_to_unduhan/', go_to_unduhan, name='go_to_unduhan'),
    path('ulasan/<tayangan_id>', open_ulasan, name='open_ulasan'),
    path('search_result', search_tayangan, name='search_tayangan'),
    path('trailer_result', search_trailer, name='search_trailer'),
    path('add_riwayat_nonton', add_riwayat_nonton, name = 'add_riwayat_nonton')
]