from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.models import Tenant
from tenants.serializers import TenantSerializer

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
