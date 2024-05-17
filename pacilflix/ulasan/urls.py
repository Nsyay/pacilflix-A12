from django.urls import path
from .views import *

app_name = 'ulasan'

urlpatterns = [
    path('tayangan/<id_tayangan>', ulasan, name='ulasan'),
    path('tayangan/<id_tayangan>', submit_ulasan, name='submit_ulasan')
]