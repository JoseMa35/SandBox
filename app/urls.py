# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('profile', views.profile, name='profile'),
    path('users', views.users, name='users'),
    path('appointments', views.appointments, name='appointments'),
    path('prescriptions', views.prescriptions, name='prescriptions'),
    path('integrations', views.integrations, name='integrations'),
    #Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
