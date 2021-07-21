from django.http import JsonResponse
from requests import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
# Create your views here.
from .models import (Specialty, Specialty_Doctor)
from .serializers import (SpecialtySerializer, SpecialtyDoctorSerializer)


# DRF CRUD AUTOMATIC
class SpecialtyList(generics.ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class SpecialtyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class SpecialtyDoctorList(generics.ListCreateAPIView):
    queryset = Specialty_Doctor.objects.all()
    serializer_class = SpecialtyDoctorSerializer


class SpecialtyDoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty_Doctor.objects.all()
    serializer_class = SpecialtyDoctorSerializer


# DRF CRUD MANUAL

class SpecialtyListView(APIView):
    def get(self, request):
        specialty_list = Specialty.objects.all().filter(is_active=True)
        data = SpecialtySerializer(specialty_list, many=True).data
        return JsonResponse(data, safe=False)


class DoctorSpecialtyListView(APIView):
    def get(self, request):
        specialty_doctor_list = Specialty_Doctor.objects.all()
        data = SpecialtyDoctorSerializer(specialty_doctor_list, many=True).data
        return JsonResponse(data, safe=False)


class DoctorSpecialtyDetailView(APIView):
    """
    specialty detail
    """

    def get(self, request, pk):
        specialty_doctor_list = Specialty_Doctor.objects.filter(specialty=pk, is_active=True)
        data = SpecialtyDoctorSerializer(specialty_doctor_list, many=True).data
        return JsonResponse(data, safe=False)
