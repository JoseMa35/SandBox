"""xiabel URL Configuration"""
from django.urls import path, include  # new

from tenants.views import TenantListView, TenantDetailView
from tenants.views import TenantStaffView, TenantStaffSpecialitiesView
from tenants.views import TenantStaffDoctorsBySpecialityView, TenantStaffDoctorsView
from tenants.views import TenantStaffDoctorScheduleView
from tenants.views import BookingView
from tenants import views

urlpatterns = [
    path('v1/tenants/', TenantListView.as_view()),
    path('v1/tenant/<pk>', TenantDetailView.as_view()),
    path('v1/tenant/<pk>/staff', TenantStaffView.as_view()),
    path('v1/tenant/<pk>/staff/specialties', TenantStaffSpecialitiesView.as_view()),
    path('v1/tenant/<pk>/staff/specialty/<specialty_id>/doctors', TenantStaffDoctorsBySpecialityView.as_view()),
    path('v1/tenant/<pk>/staff/doctors', TenantStaffDoctorsView.as_view()),
    path('v1/doctor/<pk>/schedule', TenantStaffDoctorScheduleView.as_view()),
    path('v1/booking/', BookingView.as_view())
    
    # path('v1/doctor/<doctor_id>/booking'),

]
