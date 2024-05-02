from django.urls import path
from .views import *

urlpatterns = [
    path('kelola/', kelola_langganan, name='kelola_langganan'),
    path('beli/', beli_langganan, name='beli_langganan'),
]