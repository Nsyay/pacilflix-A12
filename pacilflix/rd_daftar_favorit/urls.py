from django.urls import path
from .views import *

app_name = 'daftar_favorit'

urlpatterns = [
    path('', daftar_favorit, name='daftar_favorit'),
]