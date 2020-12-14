from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name


class SiteDetails(models.Model):
    site =  models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    salt = models.BinaryField(max_length=32)
    encryptedPass = models.BinaryField(max_length=200)
    user = models.ForeignKey (User, on_delete = models.CASCADE)

    def __str__(self):
        return self.id