from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('AccountsPayable/', AccountsPayable_list, name='AccountsPayable'),
    path('c/AccountsPayable/', Accounts_Create, name='Accounts_Create'),
    path('AccountsPayable/upt/<int:id_Accounts>/', update_Accounts, name='update_Accounts'),  # Atualizar cliente
    path('AccountsPayable/del/<int:id_Accounts>/', delete_Accounts, name='delete_Accounts'),
    path('AccountsPayable/get/<int:id_Accounts>/', get_Accounts, name='get_Accounts'),
    path('AccountsReceivable/', AccountsReceivable_list, name='AccountsReceivable'),
    path('c/AccountsReceivable/', AccountsReceivable_Create, name='AccountsReceivable_Create'),

    path('AccountsReceivable/upt/<int:id_Accounts>/', update_AccountsReceivable, name='update_AccountsReceivable'),  # Atualizar cliente
    path('AccountsReceivable/del/<int:id_Accounts>/', delete_AccountsReceivable, name='delete_AccountsReceivable'),
    path('AccountsReceivable/get/<int:id_Accounts>/', get_AccountsReceivable, name='get_AccountsReceivable'),

    path('accounts_list/<int:id_accounts>/',Accounts_list,name='Accounts_list'),
    path('delete_payments/<int:id>/',deletePayment_Accounts,name='delete_payments')
]