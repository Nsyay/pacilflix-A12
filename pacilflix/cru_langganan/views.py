from django.shortcuts import render

# Create your views here.

def kelola_langganan(request):
    return render(request, 'kelola_langganan.html')

def beli_langganan(request):
    return render(request, 'beli_langganan.html')