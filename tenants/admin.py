from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from tenants.models import Booking, BookingDetail, BookingDetailFile, Schedule, ScheduleTimeFrame, Staff, Tenant, \
    TenantSettings
from commons.models import Specialty

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

class ScheduleTimeFrameStackedInline(admin.StackedInline):
    model = ScheduleTimeFrame

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    inlines = [ScheduleTimeFrameStackedInline]

class BookingDetailFileStackedInline(NestedStackedInline):  # one
    model = BookingDetailFile
    extra = 1
    fk_name = 'booking_detail'
    
class BookingDetailStackedInline(NestedStackedInline):  # TOP
    model = BookingDetail
    extra = 1
    fk_name = 'booking_id'
    inlines = [BookingDetailFileStackedInline]

@admin.register(Booking)
class BookingAdmin(NestedModelAdmin):
    model = Booking
    inlines = [BookingDetailStackedInline]

@admin.register(BookingDetailFile)
class BookingDetailFileAdmin(admin.ModelAdmin):  # TOP
    model = BookingDetailFile
