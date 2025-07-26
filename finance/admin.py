from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentMethod_Accounts)
class PaymentMethod_AccountsAdmin(admin.ModelAdmin):
    pass
