from tenants.models import Tenant, TenantSettings, Staff
from accounts.models import User, Profile 

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

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')