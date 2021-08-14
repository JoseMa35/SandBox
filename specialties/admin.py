from django.contrib import admin

# Register your models here.  
from tenants.utils import tenant_from_request



 
    # def get_queryset(self, request, *args, **kwargs):
    #     queryset = super().get_queryset(request, *args, **kwargs) 
    #     tenant = tenant_from_request(request)
    #     queryset = queryset.filter(tenant=tenant)
    #     return queryset

    # def save_model(self, request, obj, form, change): 
    #     tenant = tenant_from_request(request) 
    #     obj.tenant = tenant 
    #     super().save_model(request, obj, form, change)