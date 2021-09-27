from checkOut.api.serializers import ItemSerializer
from typing import ContextManager
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
#from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from checkOut.models import Item
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer,StaticHTMLRenderer
from django.template import loader, context
from django.shortcuts import get_object_or_404, redirect, render
import uuid



# SDK de Mercado Pago
import mercadopago

    # Agrega credenciales
#sdk = mercadopago.SDK("TEST-6367338741216916-081714-571bcf58c036d48cd8265c82a4e3a894-417944042")


class MercadoPagoApiView(APIView):
# Crea un ítem en la preferencia
    #SDK_MERCADO = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336") 
    SDK_MERCADO_Jose = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336")  

    def post(self, request):
        print(" datos a recibir ", request.data)
        preference_data = {
            "items": [
                {
                    "title": "Mi producto",
                    "quantity": 1,
                    "unit_price": 750.76,
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8996/success/",
                "failure": "http://127.0.0.1:8996/failure/",
                "pending": "http://127.0.0.1:8996/pendings/"
            },
            "auto_return": "approved"
        }
        #preference_response = sdk.preference().create(preference_data)
        preference_response = self.SDK_MERCADO_Jose.preference().create(preference_data)
        preference = preference_response["response"]
        print("data preference", preference)
      
        return Response(
            {
                "sandbox_init_point" : preference["sandbox_init_point"],
                "init_point": preference["init_point"],
                "payment_id": preference["id"]
            } # paso 4 devolvermos las url obtenedias en la creacion de preferencia
            )



class Refund(APIView):

    SDK_MERCADO_Jose = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336")  

    def post(self, request):
        print(" datos a recibir ", request.data)
        payment_data  = {
            "status": "canceled"   
        }
        payment_id= MercadoPagoApiView.payment_id
        payment_response = self.SDK_MERCADO_Jose.payment().update(payment_id, payment_data)
        payment = payment_response["response"]
        refund_response = self.SDK_MERCADO_Jose.refund().create(payment_id)
        refund = refund_response["response"]

    def listAll(self, request):
        
        refunds_response = self.SDK_MERCADO_Jose.refund().list_all(payment_id)
        refunds = refunds_response["response"]
    


      
