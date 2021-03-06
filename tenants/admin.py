from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from tenants.models import (
    Booking, 
    BookingDetail, 
    BookingDetailFile, 
    Schedule, 
    ScheduleTimeFrame, 
    Staff, 
    Tenant,
    TenantSettings, 
    BookingDoctorDetail,
    BookingDoctorDetailFile
    

)
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

class BookingDoctorDetailFileStackedInline(NestedStackedInline):
    model = BookingDoctorDetailFile
    extra = 1
    fk_name ="booking_doctor_detail"

class BookingDoctorDetailStackedInline(NestedStackedInline):
    model = BookingDoctorDetail
    extra = 1
    fk_name ="booking_detail"
    inlines = [
        BookingDoctorDetailFileStackedInline
    ]

class BookingDetailStackedInline(NestedStackedInline):  # TOP
    model = BookingDetail
    extra = 1
    fk_name = 'booking_id'
    inlines = [
        BookingDetailFileStackedInline, 
        BookingDoctorDetailStackedInline,
        
        ]

@admin.register(Booking)
class BookingAdmin(NestedModelAdmin):
    model = Booking
    inlines = [BookingDetailStackedInline]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form  = super().get_form(request, obj=obj, change=change, **kwargs)
        def is_multipart(self):
            return True
        form.is_multipart=is_multipart
        return form

@admin.register(BookingDetailFile)
class BookingDetailFileAdmin(admin.ModelAdmin):  # TOP
    model = BookingDetailFile

@admin.register(BookingDoctorDetail)
class BookingDoctorDetailAdmin(admin.ModelAdmin):
    model= BookingDoctorDetail
    label = [
        "booking_detail_doctor"
        "file_doctor",
    ]
@admin.register(BookingDoctorDetailFile)
class BookingDoctorDetailFileAdmin(admin.ModelAdmin):
    model= BookingDoctorDetailFile

