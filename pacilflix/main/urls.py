from django.urls import path
from main.views import show_main, logout_view

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('logout/', logout_view, name='logout'),
]