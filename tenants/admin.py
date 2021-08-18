from django.contrib import admin
from tenants.models import Tenant, TenantSettings, Staff
from commons.models import Specialty


# # Register your models here.
# @admin.register(Specialty)
# class SpecialtyAdmin(admin.ModelAdmin):
#   pass


class TenantSettingsOfficerStackedInline(admin.StackedInline):
    model = TenantSettings

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    inlines = [TenantSettingsOfficerStackedInline]
    #inlines = [TenantSettingsTabularInline, ]
    

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'specialty', 'doctors_count')
    filter_horizontal = ('doctors',)
    list_filter = ('tenant',)
