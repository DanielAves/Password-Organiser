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
    def __init__(self,site = "",salt = "",encryptedPass = "",userName = ""):
        self.site = site
        self.salt = salt
        self.encryptedPass = encryptedPass
        self.userName = userName




def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:

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

def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'passwords/dashboard.html')

def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        form = CreateUserForm() 
        print("here")

        if request.method == 'POST': 
            form = CreateUserForm(request.POST)
            print(form)
            if form.is_valid(): 
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                form = CreateUserForm()
                return redirect('login')

        context = {'form':form}
        return render(request, 'passwords/register.html',context)

@login_required(login_url='login')
def SavedPassword(request):

    currentUser = request.user 

    if request.method == 'POST':
        password = request.POST.get('password')
        passInstance = encryptPassword(request,password)
        #print(passInstance.encryptedPass)

        site = request.POST.get('site')
        username = request.POST.get('username')
        print(len(passInstance.salt))
        newDetails = SiteDetails(site = site, username = username, salt = passInstance.salt, encryptedPass = passInstance.encryptedPass, user = currentUser)
        newDetails.save()
        #newRating = Rating(moduleinstance = moduleinstance, user_id = request.user.id, rating = rating, professor_id = professorID)
        #newRating.save()
        #passwords = Password.objects.all()
        return redirect(SavedPassword)
    


    # if request.method == 'POST':
    #     print("here in post request method")
    #     site = request.POST.get('site')
    #     print(site)
    #     print(request.POST.get('site'))
    #     print(request.POST.get('username'))
    #     print(request.POST.get('password'))

       
    currentUser = request.user
    emptyList = decryptPassword(request)
    for obj in emptyList:
        print(obj.encryptedPass)
    #print(emptyList.encryptedPass)
    passwords = SiteDetails.objects.all() 
    #print(request.user.password)

    return render(request,'passwords/savedPassword2.html', {'list':emptyList})
# Create your views here.

@login_required(login_url='login')
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




def storePassword():
    print("hello")

def decryptPassword(request):
    currentUser = request.user
    details = SiteDetails.objects.filter(user_id = currentUser.id)
    detailsList = []
    for each in details:
        test = each.salt
        #salt = os.urandom(32)
        print(test)
        #print(salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=test,
            iterations=100000, 
            backend=default_backend()
        )

        secretKey = settings.SECRET_KEY.encode()
        key = base64.urlsafe_b64encode(kdf.derive(secretKey))
        f = Fernet(key) 

        try:
            decrypted = f.decrypt(each.encryptedPass)
            print("valid key - successfully decrypted")



            print(decrypted)
            detailsList.append(passwordDetails(each.site,each.salt,decrypted.decode(),each.username))

            
        except InvalidToken as e:
            print("Invalid Key - Unsucessfully decrypted")
        

        
    for obj in detailsList:
        print(obj.encryptedPass)
    return(detailsList)

def encryptPassword(request,enteredPassword):

    passInstance = passwordDetails()


    # if request.method == 'POST':
    #     site = request.POST.get('site')
    #     username = request.post.get('username')
    #     enteredPassword = request.POST.get('password')

    currentUser = request.user 
    #enteredPassword = "UsersloginPass2"

    #enteredPassword = enteredPassword.encode()

    #salt = "b'\xd9\xe2\x1eS\x17\x15e\xee\x85\xe5\xac\xfb\xe4o\x9d\x05'".encode()
    passInstance.salt = os.urandom(32)
    
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

    # passInstance.salt = passInstance.salt.encode('utf8')
    # passInstance.encryptedPass = passInstance.encryptedPass.encode('utf8')



    #encrypted = "gAAAAABfRpB2D1NWxQds0xPwSJCoa9w60IX0YLIDCRwJbj1EWD0EPG9y1KiBNQ5dob1knWE0LhceFUNaAxrGi7rXlrKxgxVYHLTg02Nst8d6WwFAHub3M1Q=".encode()
    #This will be stored alongside the password

    try:

        decrypted = f.decrypt(passInstance.encryptedPass)
        print("valid key - successfully decrypted")
    except InvalidToken as e:
        print("Invalid Key - Unsucessfully decrypted")

    #print(decrypted.decode())


    return passInstance