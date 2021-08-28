from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from checkOut.models import  Item
from .serializers import ItemSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404, redirect




class ItemViewSet(viewsets.ViewSet):

    def list(self,request):
        if request.method=='GET':
            queryset = Item.objects.all()
            serializer = ItemSerializer(queryset, many= True)
            return Response(serializer.data)
        elif request.method=='POST':
            print(request.data)    

   
    def post(self, request):
        profile = get_object_or_404(Item)
        #serializer= ItemSerializer(Item)  
        serializer= ItemSerializer(data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors)  
        #return redirect('articulos')    
          


# def itemViewSet(request):
#     if request.method =='GET':
#         queryset = Item.objects.all()
#         serializer = ItemSerializer(queryset, many= True)
#         return Response(serializer.data)
    
#     elif request.method =='POST':
#         print(request.data)  

# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer