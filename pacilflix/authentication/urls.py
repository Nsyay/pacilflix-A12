from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]