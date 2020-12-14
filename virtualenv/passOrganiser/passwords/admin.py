from django.contrib import admin

from .models import Customer, SiteDetails

admin.site.register(Customer)
admin.site.register(SiteDetails)

# Register your models here.
