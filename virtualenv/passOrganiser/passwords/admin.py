from django.contrib import admin

from .models import Customer, Password

admin.site.register(Customer)
admin.site.register(Password)

# Register your models here.
