from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from commons.serializers import SpecialtySerializer
from rest_framework.permissions import  AllowAny
from tenants import serializers
from tenants.models import Schedule, Staff, Tenant, Booking
from tenants.serializers import DoctorSerializer, ScheduleSerializer, ScheduleTimeFrameSerializer, StaffSerializer, \
    TenantSerializer, BookingSerializer, BookingDetailSerializer, TenantStaffSerializer
from rest_framework import filters
from accounts.models import Profile, User

class TenantListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = Tenant.objects.all()
        serializer = TenantSerializer(tenant, many=True)
        return Response(serializer.data)


class TenantDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    # search_fields = ['last_name']
    # filter_backends = (filters.SearchFilter,)

    def get(self, request, pk):
        tenant = Tenant.objects.filter(subdomain_prefix=pk).first()
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)


class TenantStaffView(APIView):

    def get(self, request, pk):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        specialties = []
        for s in staff:
            doctor_serializer = DoctorSerializer(s.doctors, many=True)
            specialties.append({
                "title": s.specialty.name,
                "doctors": doctor_serializer.data
            })
        return Response(specialties)


class TenantStaffSpecialitiesView(APIView):
    def get(self, request, pk):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        specialties = []
        for s in staff:
            specialties.append(s.specialty)
        specialty_serializer = SpecialtySerializer(specialties, many=True)
        return Response(specialty_serializer.data)


class TenantStaffDoctorsBySpecialityView(APIView):
    def get(self, request, pk, specialty_id):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).filter(specialty_id=specialty_id).all()
        doctors = []
        for s in staff:
            doctor_serializer = DoctorSerializer(s.doctors, many=True)
            docs = doctor_serializer.data
            doctors += docs
        print(doctors)
        return Response(doctors)


# Lista de todos los doctores por Tenant
class TenantStaffDoctorsView(APIView):

    def get(self, request, pk):
        doctors = []

        if self.request.query_params.get("q") !=None:
            query = self.request.query_params.get("q")
            staff_doctors = Staff.objects.filter(tenant__subdomain_prefix=pk)
            for s in staff_doctors:
                doctor_serializer = DoctorSerializer(s.doctors, many=True)

                docs = doctor_serializer.data

                for d in docs:
                    if query in d['profile']['full_name']:
                        doctors.append(d)
            return Response(doctors)
        else:
            staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
            for s in staff:
                print(s.specialty)
                doctor_serializer = DoctorSerializer(s.doctors, many=True)
                docs = doctor_serializer.data
                for i in range(0, len(docs)):
                    # esto funciona
                    docs[i]['specialty_id'] = s.specialty.id
                    docs[i]['specialty_name'] = s.specialty.name
            
                doctors += docs
            return Response(doctors)

class TenantStaffDoctorScheduleView(APIView):
    def get(self, request, pk):

        schedule = Schedule.objects.filter(doctor_id=pk).first()

        if 'date' in request.GET != None:
            timeframes = schedule.time_frames.filter(date=request.GET['date']).all()
        else:
            timeframes = schedule.time_frames.all()

        serializer = ScheduleTimeFrameSerializer(timeframes, many=True)
        return Response(serializer.data)


class TenantStaffDoctorBookingView(APIView):

    def post(self, request, pk):
        # doctor = User.objects.filter(id=pk).first()
        pass


class BookingView(APIView):
    
    permission_classes=(AllowAny,)

    def get(self, request, pk=None, form=None):
        if pk:
            booking = get_object_or_404(BookingSerializer, id=pk)
            serializer = BookingSerializer(booking, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else: 
            booking = Booking.objects.all()
            serializer = BookingSerializer(booking, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = BookingSerializer(instance=instance)
        
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
