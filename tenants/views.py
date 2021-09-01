from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from commons.serializers import SpecialtySerializer

from tenants.models import Schedule, Staff, Tenant, Booking
from tenants.serializers import DoctorSerializer, ScheduleSerializer, ScheduleTimeFrameSerializer, StaffSerializer, \
    TenantSerializer, BookingSerializer, BookingDetailSerializer, TenantStaffSerializer


class TenantListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = Tenant.objects.all()
        serializer = TenantSerializer(tenant, many=True)
        return Response(serializer.data)


class TenantDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tenant = Tenant.objects.filter(subdomain_prefix=pk).first()
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)


class TenantStaffView(APIView):

    def get(self, request, pk):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        specialties = {}
        for s in staff:
            doctor_serializer = DoctorSerializer(s.doctors, many=True)
            specialties[s.specialty.name] = doctor_serializer.data
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

        #fix
        staff = Staff.all()
        doctors = []

        for s in staff:
            print(s.specialty)
            doctor_serializer = DoctorSerializer(s.doctors, many=True)
            docs = doctor_serializer.data
            for i in range(0, len(docs)):
                # esto funciona
                docs[i]['specialty_id'] = s.specialty.id
                docs[i]['specialty_name'] = s.specialty.name
                # error
                # docs[i]['specialty'] = s.specialty
            #doctors += zip(docs, s.specialty)
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
        data_booking = {
            'doctor_id': request.data.get('doctor_id'),
            'client_id': request.data.get('client_id'),
            'virtual_profile': request.data.get('virtual_profile'),
            'status': request.data.get('status'),
            'datetime': request.data.get('datetime'),
            'meeting_link': request.data.get('meeting_link'),
            'created_at': request.data.get('created_at'),
            'updated_at': request.data.get('updated_at'),
        }

        data_detail = {
            "has_disability": request.data.get("detail", {}).get("has_disability", None),
            "smoke": request.data.get("detail", {}).get("smoke", None),
            "drink": request.data.get("detail", {}).get("drink", None),
            "allergic": request.data.get("detail", {}).get("allergic", None),
            "extra_info": request.data.get("detail", {}).get("extra_info", None),
            "brief_description": request.data.get("detail", {}).get("brief_description", None),
            "created_at": request.data.get("detail", {}).get("created_at",None),
            "updated_at": request.data.get("detail", {}).get("updated_at", None),
        }

        serializer = BookingSerializer(data=data_booking)

        if serializer.is_valid():
            booking = serializer.save()

            data_detail["booking_id"] = booking.pk
    
            detail_seriliezer = BookingDetailSerializer(data=data_detail)

            if detail_seriliezer.is_valid():
                detail_seriliezer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
