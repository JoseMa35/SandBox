from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

from .models import (Gender, Document_Type)
from .serializers import (GenderSerializer, DocumentTypeSerializer)


class GenderListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        gender = Gender.objects.all()
        data = GenderSerializer(gender, many=True).data
        return Response(data)


class GenderDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        gender = get_object_or_404(Gender, pk=pk)
        data = GenderSerializer(gender, many=True).data
        return Response(data)


class DocumentTypeListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        document = Document_Type.objects.all()
        data = DocumentTypeSerializer(document, many=True).data
        return Response(data)


class DocumentTypeDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        document = get_object_or_404(Document_Type, pk=pk)
        data = DocumentTypeSerializer(document, many=True).data
        return Response(data)
