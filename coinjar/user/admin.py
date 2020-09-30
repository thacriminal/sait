from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
#admin.site.register(get_user_model(),UserAdmin)

class UserAdmin(admin.ModelAdmin):
    search_fields = ('phone','token')

admin.site.register(get_user_model(),UserAdmin)
class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ('user__userlogin',)

admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Contacts)
admin.site.register(TransactionsHistory)

admin.site.register(Wallets)