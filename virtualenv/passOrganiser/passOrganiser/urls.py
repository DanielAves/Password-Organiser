
from django.contrib import admin
from django.urls import path, include
#from passwords.views import LoginPage, HomePage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('passwords.urls')),
]
