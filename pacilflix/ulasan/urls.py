from django.urls import path
from .views import *

urlpatterns = [
    path('', ulasan, name='ulasan'),
]