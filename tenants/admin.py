from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from tenants.models import Tenant, TenantSettings, Staff, Booking, BookingDetail, BookingDetailFile
from commons.models import Specialty



# # Register your models here.
# @admin.register(Specialty)
# class SpecialtyAdmin(admin.ModelAdmin):
#   pass


class TenantSettingsOfficerStackedInline(admin.StackedInline):
    model = TenantSettings

class BookingDetailFileStackedInline(NestedStackedInline):
    model = BookingDetailFile

class BookingDetailStackedInline(NestedStackedInline):
    model = BookingDetail
    inlines = [BookingDetailFileStackedInline]



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

@admin.register(Booking)
class BookingAdmin(NestedModelAdmin):
    model = Booking
    inlines = [BookingDetailStackedInline]