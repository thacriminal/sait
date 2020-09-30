from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
import requests, json, logging
import urllib.request as urllib2
from django import template
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from .forms import *
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate,logout, login as dj_login
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.conf import settings
from rest_framework.views import APIView
from datetime import datetime, tzinfo, timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
import requests
from django.views import View
import json, random, string
import time
from user.models import Currency,Contacts,Wallets,TransactionsHistory

def get_random_string(length):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(length)))
    sample_str += ''.join((random.choice(string.digits) for i in range(3)))
    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string

currency_data = {
    "BTC": {"simbol":"BTC","name":"Bitcoin","slug":"Bitcoin"},
    "ETH": {"simbol":"ETH","name":"Ethereum","slug":"Ether"},
    "XRP": {"simbol":"XRP","name":"XRP","slug":"Ripple XRP"},
    "LTC": {"simbol":"LTC","name":"Litecoin","slug":"Litecoin"},
    "USDC": {"simbol":"USDC","name":"USDC","slug":"USD Coin"},
    "DAI": {"simbol":"Dai","name":"Dai","slug":"Maker Dai"},
    "ZRX": {"simbol":"ZRX","name":"0x","slug":"0x Token"},
    "BAT": {"simbol":"BAT","name":"BAT","slug":"Basic Attention Token"},
    "XLM": {"simbol":"XLM","name":"XLM","slug":"Stellar Lumens"},
}

class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        
        currency = request.GET.get("currency",None)
        user_currency = Currency.objects.filter(user=user)
        a = []
        for i in user_currency:
            a.append(i.slug)
        print(a)
        print(currency)
        index = 'is-active'
        if currency and len(user_currency.filter(simbol__icontains=currency))==0:
            data = currency_data[currency.upper()]
            cur = Currency(user=user,simbol=data["simbol"],name=data["name"],slug=data["slug"])
            cur.save()
            return HttpResponseRedirect('/')
        user_currency = Currency.objects.filter(user=user)
        return render(request, 'index.html',locals())
    def post(self,request):
        pass

class ContactsView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        contacts = 'is-active'
        form = AuthenticationForm()
        search = request.GET.get("search",None)
        search_flag = False
        contact_list = Contacts.objects.filter(user=user)
        

        if search:
            search = search.replace("@","")
            if len(contact_list.filter(contact_user__userlogin="@"+search))>0:
                search_flag = False
                error_text = "You can't add a contact twice"
            else:
                searchcontact = UserModel.objects.filter(userlogin__icontains="@"+search).first()
                if searchcontact == None:
                    search_flag = False
                else:
                    search_flag = True
            
        
        return render(request, 'contacts.html',locals())
    def post(self,request):
        login=request.POST['login']
        search_contact = UserModel.objects.filter(userlogin=login).first()
        if search_contact:
            contact = Contacts(user=request.user,contact_user=search_contact,full_name=request.POST['full_name'])
            contact.save()
        return HttpResponseRedirect('/contacts/')

class PaymentView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        tab_index = request.GET.get("tab",None)
        payments = 'is-active'
        form = AuthenticationForm()
        user_currency = Currency.objects.filter(user=user)
        currency_btc = Currency.objects.filter(user=user,simbol="BTC").first()
        contact_list = Contacts.objects.filter(user=user)   
        
        return render(request, 'payment.html',locals())
    def post(self,request):
        login=request.POST['login']
        search_contact = UserModel.objects.filter(userlogin=login).first()
        if search_contact:
            contact = Contacts(user=request.user,contact_user=search_contact,full_name=request.POST['full_name'])
            contact.save()
        return HttpResponseRedirect('/payment/')
class TransactionView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        currency = request.GET.get("currency")
        amount = float(request.GET.get("amount"))
        contact = request.GET.get("contact")
        user_currency = Currency.objects.filter(user=user,simbol=currency).first()
        if user_currency:
            if user_currency.balance >= amount:
                user_currency.balance = user_currency.balance -amount
                user_currency.save()
                t = TransactionsHistory()
                t.user = user
                t.wallet = currency
                t.amount = amount
                t.status = "Peding"
                t.description = "Transaction to "+contact
                t.save()
        return HttpResponse("OK")
class AccountDetailView(View):
    def get(self,request,uuid):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        index = 'is-active'
        form = AuthenticationForm()
        currency = Currency.objects.get(user=user,uid=uuid)
        wallet = Wallets.objects.filter(name=currency.simbol).first()
        transactions = TransactionsHistory.objects.filter(user=user,wallet=currency.simbol)
        trans = True
        if len(transactions)>0:
            trans=False
        user_currency = Currency.objects.filter(user=user).exclude(uid=uuid) 
        
        return render(request, 'account_detail.html',locals())

class SettingsView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/users/sign_in/')
        user = request.user
        settings = 'is-active'
        currency = request.GET.get("currency",None)
        aviable_currency = ["USD","AUD","GBP","EUR"]
        if currency and currency.upper() in aviable_currency:
            user.reference_currency = currency
            user.save()
            return HttpResponseRedirect('/settings/')
        form = AuthenticationForm()
        return render(request, 'settings.html',locals())
    def post(self,request):
        login=request.POST['login']
        
        return HttpResponseRedirect('/settings/')

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated == True:
            return HttpResponseRedirect('/')
        form = AuthenticationForm()
        return render(request, 'login.html',locals())
    def post(self,request):
        if request.user.is_authenticated == True:
            return HttpResponseRedirect('/')
        form = AuthenticationForm(data=request.POST)
        
        response = render(request,'login.html',locals())
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return HttpResponseRedirect('/')
        print(form.errors)
        return response

class RegisterView(View):
    def get(self,request):
        print(111)
        form = RegisterForm()
        return render(request, 'register.html',locals())
    def post(self,request):
        form = RegisterForm(request.POST)
        response = render(request, 'register.html',locals())
        if form.is_valid():
            f = form.save(commit=False)
            f.username = form.cleaned_data.get('email')
            f.userlogin = "@"+get_random_string(5)
            f.customer_number = random.randint(10000000, 99999999)
            f.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user)
            return HttpResponseRedirect('/')
        else:
            print("Eroor")
        return response
class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect("/users/sign_in/")