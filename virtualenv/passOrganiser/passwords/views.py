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
from django.contrib.auth.decorators import login_required
import os

class passwordDetails:
    def __init__(self,id = "", site = "",salt = "",encryptedPass = "",userName = ""):
        self.id = id
        self.site = site
        self.salt = salt
        self.encryptedPass = encryptedPass
        self.userName = userName

def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('savedPassword')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username = username, password= password)

            if user is not None: 
                login(request, user)
                return redirect('savedPassword')
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'passwords/login.html')
        return render(request, 'passwords/login.html')

def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'passwords/settings.html')

def Register(request):
    if request.user.is_authenticated:
        return redirect('savedPassword')
    else:
        form = CreateUserForm() 
        if request.method == 'POST': 
            form = CreateUserForm(request.POST)
            if form.is_valid(): 
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'passwords/register.html',context)

@login_required(login_url='login')
def SavedPassword(request):

    currentUser = request.user 

    if request.method == 'POST':
        password = request.POST.get('password')
        site = request.POST.get('site')
        username = request.POST.get('username')

        if (password and site and username != ""):
            passInstance = encryptPassword(request,password)
            newDetails = SiteDetails(site = site, username = username, salt = passInstance.salt, encryptedPass = passInstance.encryptedPass, user = currentUser)
            newDetails.save()
        else:
            messages.warning(request, 'Information must be entered in each column')

        return redirect(SavedPassword)
    
    siteDetailsList = decryptPassword(request)
    return render(request,'passwords/savedPassword.html', {'list':siteDetailsList})


@login_required(login_url='login')
def Settings(request):
    return render(request, 'passwords/settings.html')


def decryptPassword(request):
    currentUser = request.user
    details = SiteDetails.objects.filter(user_id = currentUser.id)
    detailsList = []
    for each in details:
        salt = each.salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000, 
            backend=default_backend()
        )

        secretKey = settings.SECRET_KEY.encode()
        key = base64.urlsafe_b64encode(kdf.derive(secretKey))
        f = Fernet(key) 

        try:
            decrypted = f.decrypt(each.encryptedPass)
            #Create a new list with the decrypted passwords
            detailsList.append(passwordDetails(each.id,each.site,each.salt,decrypted.decode(),each.username))
        except InvalidToken as e:
            print("Invalid Key - Unsucessfully decrypted")
    
    return(detailsList)


def encryptPassword(request,enteredPassword):


    passInstance = passwordDetails()
    currentUser = request.user 

    #Generate random salt
    passInstance.salt = os.urandom(32)
    
    #Use SHA256 with salt to encrypt password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=passInstance.salt,
        iterations=100000, 
        backend=default_backend()
    )
    
    #Method of getting key based on entered password
    #key = base64.urlsafe_b64encode(kdf.derive(enteredPassword))

    secretKey = settings.SECRET_KEY.encode()
    key = base64.urlsafe_b64encode(kdf.derive(secretKey))
    f = Fernet(key) 
    passInstance.encryptedPass = f.encrypt(enteredPassword.encode())

    try:
        decrypted = f.decrypt(passInstance.encryptedPass)
        print("valid key - successfully decrypted")
    except InvalidToken as e:
        print("Invalid Key - Unsucessfully decrypted")

    return passInstance


def DeleteDetails(request, pk):
    details = SiteDetails.objects.filter(id = pk)
    details.delete()
    return redirect(SavedPassword)