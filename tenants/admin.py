from django.contrib import admin
from tenants.models import Tenant, Staff

# Register your models here.
@admin.register(Tenant)
class SpecialtyAdmin(admin.ModelAdmin):
  pass

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'specialty', 'doctors_count')
    filter_horizontal = ('doctors',)
    list_filter = ('tenant',)