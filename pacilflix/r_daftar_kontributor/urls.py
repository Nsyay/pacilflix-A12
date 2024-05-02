from django.urls import path
from .views import *

urlpatterns = [
    path('', kontributor, name='kontributor'),
]
