from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.models import Tenant, Staff
from tenants.serializers import TenantSerializer, TenantStaffSerializer, StaffSerializer, DoctorSerializer, \
    PatientAppointmentSerializer, PatientProfileSerializer
from commons.serializers import SpecialtySerializer
from accounts.models import User, Profile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication


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
                docs[i]['specialty'] = s.specialty
            doctors += zip(docs, s.specialty)
        return Response(doctors)


class PatientViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = request.user.pk
        serializer = PatientAppointmentSerializer(data=request.data)

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

        if serializer.is_valid():
            _profile =  serializer.validated_data['profile']
            fullname =  serializer.validated_data['profile']['full_name']
            _profile.user = request.user

            if profile is None:
                user = User.objects.get(pk=request.user.pk)
                print(_profile)
                print(fullname)
                instance = PatientProfileSerializer.save(data=_profile)

                user.profile = _profile
                # user.profile.save()
                # user.profile.full_name = _profile.validated_data.get('full_name', _profile.full_name)
                # user.profile.gender = _profile.validated_data.get('gender', _profile.gender)
                # user.profile.age = _profile.validated_data.get('age', _profile.age)
                # user.profile.document_type = _profile.validated_data.get('document_type', _profile.document_type)
                # user.profile.document = _profile.validated_data.get('document', _profile.document)
                # user.profile.is_disability = _profile.validated_data.get('is_disability', _profile.is_disability)
                # user.profile.is_smoker = _profile.validated_data.get('is_smoker', _profile.is_smoker)
                # user.profile.is_alcohol = _profile.validated_data.get('is_alcohol', _profile.is_alcohol)
                # user.profile.is_allegiance = _profile.validated_data.get('is_allegiance', _profile.is_allegiance)
                # user.profile.allegiance_detail = _profile.validated_data.get('allegiance_detail', _profile.allegiance_detail)
                user.profile.save()
            else:
                profile = _profile
                profile.save()
                # PatientProfileSerializer.update(self, profile, validated_data=_profile)

            print(profile)

            # serializer_profile.update()
            # serializer.save()
            # if (serializer.is_valid()):
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"serializer.data, status=status.HTTP_201_CREATED"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
