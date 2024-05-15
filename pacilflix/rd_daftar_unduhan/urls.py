from django.urls import path
from .views import *

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', daftar_unduhan, name='daftar_unduhan'),
    path('hapus_unduhan/', hapus_unduhan, name='hapus_unduhan')
]