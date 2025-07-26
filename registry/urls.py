from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('pessoa/cadastrar/', Client_Create, name='Client_Create'),
    path('pessoa/', client_list, name='Client'),
    path('b-prsn/', buscar_clientes, name='buscar_clientes'),
    path('pessoa/deletar/<int:id_client>/', delete_client, name='delete_client'),

    ]
