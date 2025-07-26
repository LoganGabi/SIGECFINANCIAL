from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass

@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    pass



@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

