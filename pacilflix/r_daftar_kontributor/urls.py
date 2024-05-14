from django.urls import path
from .views import *

app_name = 'daftar-kontributor'

urlpatterns = [
    path('', kontributor, name='kontributor'),
]
