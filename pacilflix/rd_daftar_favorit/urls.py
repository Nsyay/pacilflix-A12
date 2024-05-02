from django.urls import path
from .views import *

urlpatterns = [
    path('', daftar_favorit, name='daftar_favorit'),
]