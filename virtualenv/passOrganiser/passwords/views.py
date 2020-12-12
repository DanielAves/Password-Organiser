from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
import os


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(username = username, password= password)

        if user is not None: 
              login(request, user)
              print("Success")
              return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'passwords/login.html')
    return render(request, 'passwords/login.html')

def HomePage(request):
    return render(request, 'passwords/dashboard.html')

def Register(request): 
    form = CreateUserForm() 


    if request.method == 'POST': 
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)

            form = CreateUserForm()
            return redirect('login')

    context = {'form':form}
    return render(request, 'passwords/register.html',context)

def SavedPassword(request):

    if request.method == 'POST':
        password = request.POST.get('password')
        encrypted = encryptPassword(request,password)
        #print(encrypted)
        passwords = Password.objects.all()
        return redirect(SavedPassword)
    passwords = Password.objects.all()


    # if request.method == 'POST':
    #     print("here in post request method")
    #     site = request.POST.get('site')
    #     print(site)
    #     print(request.POST.get('site'))
    #     print(request.POST.get('username'))
    #     print(request.POST.get('password'))

       
    currentUser = request.user 
    #print(request.user.password)

    return render(request,'passwords/savedPassword2.html', {'list':passwords})
# Create your views here.


def storePass(request):
    context = {}

    if request.method == 'POST':
        site = request.POST.get('site')

        print(request.POST.get('site'))
        print(request.POST.get('username'))
        print(request.POST.get('password'))

    #password = request.POST.get('password')




    encryptPassword(request,"EnteredPasswordToSave")

    return render(request, 'passwords/storePassword.html')




def encryptPassword(request,enteredPassword):


    # if request.method == 'POST':
    #     site = request.POST.get('site')
    #     username = request.post.get('username')
    #     enteredPassword = request.POST.get('password')

    currentUser = request.user 
    #enteredPassword = "UsersloginPass2"

    #enteredPassword = enteredPassword.encode()

    salt = "b'\xd9\xe2\x1eS\x17\x15e\xee\x85\xe5\xac\xfb\xe4o\x9d\x05'".encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000, 
        backend=default_backend()
    )
    #Method of getting key based on entered password
    #key = base64.urlsafe_b64encode(kdf.derive(enteredPassword))

    secretKey = settings.SECRET_KEY.encode()
    key = base64.urlsafe_b64encode(kdf.derive(secretKey))
    f = Fernet(key) 
    encrypted = f.encrypt(enteredPassword.encode())



    #encrypted = "gAAAAABfRpB2D1NWxQds0xPwSJCoa9w60IX0YLIDCRwJbj1EWD0EPG9y1KiBNQ5dob1knWE0LhceFUNaAxrGi7rXlrKxgxVYHLTg02Nst8d6WwFAHub3M1Q=".encode()
    #This will be stored alongside the password

    try:

        decrypted = f.decrypt(encrypted)
        print("valid key - successfully decrypted")
    except InvalidToken as e:
        print("Invalid Key - Unsucessfully decrypted")

    print(decrypted.decode())


    return encrypted