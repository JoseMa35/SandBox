from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.models import Tenant, Staff
from tenants.serializers import TenantSerializer, TenantStaffSerializer, StaffSerializer, DoctorSerializer
from commons.serializers import SpecialtySerializer


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
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        doctors = []

        for s in staff:
            print(s.specialty)
            doctor_serializer = DoctorSerializer(s.doctors, many=True)
            docs = doctor_serializer.data

            for i in range(0, len(docs)):
                print(docs[i])
                docs[i]['specialty_id']= s.specialty.id
                docs[i]['specialty_name'] = s.specialty.name
            doctors += docs
        print(doctors)
        return Response(doctors)

class TenantStaffDoctorScheduleView(APIView):
    def get(self, request, pk, doctor_id):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk)
        for s in staff:
            for d in s.doctors:
                if d.id == doctor_id:
                    doctor_schedule = d.schedule
        
        doctor_serializer = DoctorSerializer(staff.doctors)
        return Response(doctor_serializer.data)

class TenantStaffDoctorBookingView(APIView):
    def post(self, request, pk, doctor_id):
        pass