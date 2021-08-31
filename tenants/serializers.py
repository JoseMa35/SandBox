from tenants.models import Schedule, ScheduleTimeFrame, Staff, Tenant, TenantSettings
from accounts.models import User, Profile
from commons.serializers import SpecialtySerializer

from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'specialty', 'doctors')


class TenantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSettings
        fields = ('color', 'logo')


class TenantSerializer(serializers.ModelSerializer):
    settings = TenantSettingsSerializer(read_only=True)

    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'settings')


class TenantStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True, many=True)

    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'staff')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ('avatar', 'user')

class DoctorSerializer(serializers.ModelSerializer):
    profile = DoctorProfileSerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile', 'specialty')

class ScheduleTimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTimeFrame
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleTimeFrameSerializer(read_only=True, many=True)
    class Meta:
        model = Schedule
        fields = ('doctor', 'schedule')
