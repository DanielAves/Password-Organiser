from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name


class Password(models.Model):
    site =  models.CharField(max_length=200)
    salt = models.CharField(max_length=16)
    encryptedPass = models.CharField(max_length=200)
    customer = models.ForeignKey (Customer, on_delete = models.CASCADE)

