from rest_framework import generics
from rest_framework.views import APIView

# Create your views here.

from .models import (Specialty, Specialty_Doctor)
from .serializers import (SpecialtySerializer, SpecialtyDoctorSerializer)


class SpecialtyList(APIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

class SpecialtyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

class SpecialtyDoctorList(APIView):
    queryset = Specialty_Doctor.objects.all()
    serializer_class = SpecialtyDoctorSerializer

class SpecialtyDoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty_Doctor.objects.all()
    serializer_class = SpecialtyDoctorSerializer

