# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(
        "v1/mercado-pago/preference/", 
        views.MercadoPagoApiView.as_view()
    ),
    path(
        "v1/mercado-pago/webhook/", 
        views.NotificationWebHookApiView.as_view()
    )
]