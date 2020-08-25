from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def LoginPage(request):
    return render(request, 'passwords/login.html')

def HomePage(request):
    return render(request, 'passwords/dashboard.html')

def SavedPassword(request):
    passwords = Password.objects.all()

    if request.method == 'POST':
        site = request.POST.get('site')

        print(site)
        print("Hello world")

    return render(request,'passwords/savedPassword.html', {'list':passwords})
# Create your views here.


def storePass(request):
    context = {}


        

    return render(request, 'passwords/storePassword.html')
