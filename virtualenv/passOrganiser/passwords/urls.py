from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name="home"),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('register/', views.Register, name="register"),
    path('savedPassword/', views.SavedPassword, name="savedPassword"),
    path('storePassword/', views.storePass, name="storePass"),
    path('deleteDetails/<str:pk>/', views.DeleteDetails, name="deleteDetails")
]