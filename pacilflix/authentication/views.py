from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Pengguna P WHERE P.username = %s AND P.password = %s", [username, password])
            user = cursor.fetchone()

        if user:
            request.session['username'] = user[0]

            # Redirect to 'tayangan:tayangan' view
            response = redirect(reverse('tayangan:tayangan'))

            # Set cookies for 'username' and 'last_login'
            response.set_cookie('username', user[0])
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Username atau Password salah. Coba lagi!')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pengguna WHERE username = %s", [username])
            users = cursor.fetchall()

        if users:
            messages.error(request, "Username yang Anda gunakan sudah tersedia.")
            context = {'form': request.POST}
            return render(request, 'register.html', context)
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO pengguna (username, password, negara_asal) VALUES (%s, %s, %s)", [username, password, negara_asal])
        
        messages.success(request, 'Akun berhasil dibuat!')
        return redirect('authentication:login')

    return render(request, 'register.html')
