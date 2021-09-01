from rest_framework.response import Response
from rest_framework.views import APIView

from commons.serializers import SpecialtySerializer

from tenants.models import Schedule, Staff, Tenant
from tenants.serializers import DoctorSerializer, ScheduleSerializer, ScheduleTimeFrameSerializer, StaffSerializer, \
    TenantSerializer, TenantStaffSerializer


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
                # esto funciona
                docs[i]['specialty_id'] = s.specialty.id
                docs[i]['specialty_name'] = s.specialty.name
                # error
                # docs[i]['specialty'] = s.specialty
            doctors += zip(docs, s.specialty)
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

