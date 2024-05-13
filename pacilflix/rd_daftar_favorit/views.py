from django.shortcuts import render

# Create your views here.
def daftar_favorit(request):
    return render(request, 'daftar_favorit.html')

def tayangan_favorit(request):
    return render(request, 'tayangan_favorit.html')