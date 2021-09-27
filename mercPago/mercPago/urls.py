"""mercPago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Pattern
from django import urls
#from checkOut.views import  ( 
    #FailPayView, ListadoItems, PendingPayView, SuccesfulPayView)
from django.contrib import admin
from django.urls import path, include
from .router import router
from checkOut.views import MercadoPagoApiView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth',include('rest_framework.urls')),
    #path('articulos/',ListadoItems.as_view(), name="listadoArticulos"),
    #path('success/',SuccesfulPayView.as_view(),name='pagoExitoso'),
    #path('pending/',PendingPayView.as_view(),name='pagoPendiente'),
    #path('failure/',FailPayView.as_view(),name='pagoDenegado'),
    path('api/mercadoPago/',MercadoPagoApiView.as_view()),
    path('api/',include(router.urls)),
    
]
