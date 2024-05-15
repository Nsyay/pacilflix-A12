from django.urls import path
from .views import *

app_name = 'daftar_favorit'

urlpatterns = [
    path('', daftar_favorit, name='daftar_favorit'),
    path('tayangan_favorit/', tayangan_favorit, name='tayangan_favorit'),
    path('hapus_daftar/', hapus_daftar, name='hapus_daftar'),
    path('hapus_tayangan_favorit/', hapus_tayangan_favorit, name='hapus_tayangan_favorit')
]