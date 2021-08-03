# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, CustomAuthToken, CustomCreateUser
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('api/signin/', CustomAuthToken.as_view(), name="signin"),
    path('api/signup/', CustomCreateUser.as_view(), name="signup"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
