from django.shortcuts import render,redirect

# Create your views here.
def show_main(request):
    return render(request, "main.html")

def logout_view(request):
    response = redirect('main:show_main')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response
