from django.urls import path
from .views import *

urlpatterns = [
    path('', tayangan, name='tayangan'),
    path('', trailer, name='trailer'),
    path('', film, name='film'),
    path('', series, name='series'),
    path('', episode, name='episode'),
]