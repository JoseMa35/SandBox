from tenants.models import Tenant, TenantSettings

from rest_framework import serializers


class TenantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSettings
        fields = ('color', 'logo')

class TenantSerializer(serializers.ModelSerializer):
  
    settings = TenantSettingsSerializer(read_only=True)
    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'settings')
