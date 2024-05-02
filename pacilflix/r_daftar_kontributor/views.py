from django.shortcuts import render

# Create your views here.
app_name = 'daftar-kontributor'

def kontributor(request):
    return render(request, 'kontributor.html')
