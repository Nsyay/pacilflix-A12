from django.urls import path
from .views import *

urlpatterns = [
    path('', daftar_unduhan, name='daftar_unduhan'),
]