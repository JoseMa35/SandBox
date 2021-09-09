# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from commons.integrations import gcalendar

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('profile', views.profile, name='profile'),
    path('users', views.users, name='users'),
    path('appointments', views.appointments, name='appointments'),
    path('doctors', views.doctors, name='doctors'),
    path('prescriptions', views.prescriptions, name='prescriptions'),
    path('specialties', views.specialties, name='specialties'),
    path('specialties/add', views.specialties, name='specialty_add'),
    path('integrations', views.integrations, name='integrations'),
    #Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    # OAUTH2 GOOGLE CALENDAR
    path("integrations/calendar/oauth2/google/redirect", gcalendar.AuthGoogle),
    path("integrations/calendar/oauth2/google/callback", gcalendar.CallbackAuthGoogle),
    path("integrations/calendar/create", gcalendar.create_calendar),
    path("integrations/calendar/detail", gcalendar.get_calendar),
    path("integrations/calendar/freebuzy", gcalendar.get_freebusy),
    path("integrations/calendar/event/list", gcalendar.list_all_events),
    path("integrations/calendar/event/freetime", gcalendar.free_time),
]
