from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import os


def LoginPage(request):
    return render(request, 'passwords/login.html')

def HomePage(request):
    return render(request, 'passwords/dashboard.html')

def SavedPassword(request):
    passwords = Password.objects.all()

    if request.method == 'POST':
        site = request.POST.get('site')

        
    currentUser = request.user 
    print(request.user.password)

    return render(request,'passwords/savedPassword.html', {'list':passwords})
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




def encryptPassword(request,password):

    currentUser = request.user 
    #enteredPassword = request.user.password
    enteredPassword = "UsersloginPass2"
    # print(enteredPassword)
    # print(password)
    enteredPassword = enteredPassword.encode()

    salt = "b'\xd9\xe2\x1eS\x17\x15e\xee\x85\xe5\xac\xfb\xe4o\x9d\x05'".encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(enteredPassword))

    f = Fernet(key) 
    # encrypted = f.encrypt(password.encode())
    # print(encrypted)


    encrypted = "gAAAAABfRpB2D1NWxQds0xPwSJCoa9w60IX0YLIDCRwJbj1EWD0EPG9y1KiBNQ5dob1knWE0LhceFUNaAxrGi7rXlrKxgxVYHLTg02Nst8d6WwFAHub3M1Q=".encode()
    #This will be stored alongside the password
    try:

        decrypted = f.decrypt(encrypted)
        print("valid key - successfully decrypted")
    except InvalidToken as e:
        print("Invalid Key - Unsucessfully decrypted")

    #print(decrypted.decode())