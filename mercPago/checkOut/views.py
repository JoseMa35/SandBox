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



# SDK de Mercado Pago
import mercadopago

# Agrega credenciales
sdk = mercadopago.SDK("TEST-6367338741216916-081714-571bcf58c036d48cd8265c82a4e3a894-417944042")

# Crea un ítem en la preferencia
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


preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
#print(preference['id'])

class ListadoItems(APIView):
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'Item_detail.html'


    def get(self, request):
        # profile = get_object_or_404(Item)
        # serializer= ItemSerializer(profile)
        items = Item.objects.all()
        return render(request,'checkOut.html',{'items':items,'preference_id':preference['id']})  

    def post(self, request):
        profile = get_object_or_404(Item)
        serializer= ItemSerializer(Item)    
        if not serializer.is_valid():
            return Response({'serializer':serializer, 'Item':Item})  
        serializer.save()
        return redirect('articulos')    

class SuccesfulPayView(APIView):

    def get(self, request):
        return render(request,'succesfulPay.html',{}) 

class FailPayView(APIView):

    def get(self, request):
        return render(request,'failurePay.html',{}) 

class PendingPayView(APIView):

    def get(self, request):
        return render(request,'pendingPay.html',{})         


# class ListadoItems(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'chekOut.html'    

#     def get(self, request):
#         queryset = Item.objects.all()
#         return Response({'Items': queryset})          

#def listadoItems(request):#lista ya serializada.

    #lista = preference_data
 
    #return JsonResponse(lista, safe=False)#como es un "non dict object" le ponemos safe false

#def listadoItems(request):
    #context = {}
    #context['segment'] = 'Items'
    #context['Items'] = Item.objects.all()
    #html_template = loader.get_template('core/checkOut.html')
    #return HttpResponse(html_template.render(context, request))



      
