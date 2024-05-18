from django.urls import path
from .views import *

app_name = 'ulasan'

urlpatterns = [
    path('tayangan/<id_tayangan>', ulasan, name='ulasan'),
    path('submit_ulasan/<id_tayangan>', submit_ulasan, name='submit_ulasan')
]