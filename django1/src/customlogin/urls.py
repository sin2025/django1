'''
Created on 2019. 1. 27.

@author: user
'''
from django.urls import path
from .views import *

app_name='cl'
#기본주소: 127.0.0.1:8000/c1/
urlpatterns=[
    #127.0.0.1:8000/c1/signup/
    path('signup/',signup, name='signup'),
    #127.0.0.1:8000/c1/signin/
    path('signin/',signin, name='signin'),
    #127.0.0.1:8000/c1/signout/
    path('signout/',signout, name='signout')
    
    ]