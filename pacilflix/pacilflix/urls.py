"""
URL configuration for pacilflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
=======
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('daftar-kontributor/', include('r_daftar_kontributor.urls')),
    path('langganan/', include('cru_langganan.urls')),
    path('daftar_favorit/', include('rd_daftar_favorit.urls')),
    path('daftar_unduhan/', include('rd_daftar_unduhan.urls'))
>>>>>>> 69ea5a7203e07ca66613db0f81e0d281a5e53bf0
]
