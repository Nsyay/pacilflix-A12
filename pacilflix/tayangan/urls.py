from django.urls import path
from .views import *

app_name = 'tayangan'

urlpatterns = [
    path('episode/', episode, name='episode'),
    path('film/', film, name='film'),
    path('series/', series, name='series'),
    path('tayangan/', tayangan, name='tayangan'),
    path('trailer/', trailer, name='trailer'),
    path('trailer_guest/', trailer_guest, name='trailer_guest')
]