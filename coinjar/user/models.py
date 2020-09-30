from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class AUser(AbstractUser):
    email = models.EmailField(max_length=250,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    customer_number = models.IntegerField(null=True,blank=True)
    reference_currency = models.CharField(default="USD",max_length=255,blank=True,null=True)
    userlogin = models.CharField(null=True,blank=True,max_length=255)
    def __str__(self):
        return str(self.userlogin)

class Currency(models.Model):
    user = models.ForeignKey(AUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True,null=True)
    simbol = models.CharField(max_length=255,blank=True,null=True)
    slug = models.CharField(max_length=255,blank=True,null=True)
    uid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    balance = models.FloatField(default=0.0000)
    balance_usd = models.FloatField(default=0.00)
    def __str__(self):
        return self.user.userlogin + " | " + self.simbol
class Contacts(models.Model):
    user = models.ForeignKey(AUser,on_delete=models.CASCADE)
    contact_user = models.ForeignKey(AUser,on_delete=models.CASCADE,related_name="contact_user",null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.user.userlogin
class Wallets(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name
class TransactionsHistory(models.Model):
    user = models.ForeignKey(AUser,on_delete=models.CASCADE)
    wallet = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateField(auto_now=True)
    amount = models.FloatField(default=0.00)
    status = models.CharField(max_length=255,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.userlogin + " | "+self.wallet+ " | "+str(self.amount)