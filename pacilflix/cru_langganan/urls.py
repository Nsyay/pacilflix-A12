from django.urls import path
from .views import *

app_name = 'langganan'

urlpatterns = [
    path('kelola_langganan', kelola_langganan, name='kelola_langganan'),
    path('create_transaction', create_transaction, name='create_transaction'),
    path('beli_langganan/<str:nama_paket>/', beli_langganan, name='beli_langganan'),
]