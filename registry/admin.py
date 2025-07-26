from django.contrib import admin
from .models import *

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(FisicPerson)
class FisicPersonAdmin(admin.ModelAdmin):
    pass

@admin.register(ForeignPerson)
class ForeignPersonAdmin(admin.ModelAdmin):
    pass

@admin.register(LegalPerson)
class LegalPersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

# Register your models here.
