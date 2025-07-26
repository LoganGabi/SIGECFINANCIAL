from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', my_login, name='login'),
    path('logout/', my_logout, name='logout'),
    path('notifications/',notifications,name='notifications'),
    path('', index, name='index'),
    path('log/', log, name='log'),
    path('log_detailed/<int:log_id>/', log_detailed, name='log_detailed'),
]
