"""xiabel URL Configuration"""
from django.urls import path, include # new

from tenants.views import TenantListView, TenantDetailView, TenantStaffView, TenantStaffSpecialitiesView, TenantStaffDoctorsBySpecialityView, TenantStaffDoctorsView

urlpatterns = [
    path('v1/tenants/', TenantListView.as_view()),
    path('v1/tenant/<pk>', TenantDetailView.as_view()),
    path('v1/tenant/<pk>/staff', TenantStaffView.as_view()),
    path('v1/tenant/<pk>/staff/specialties', TenantStaffSpecialitiesView.as_view()),
    path('v1/tenant/<pk>/staff/specialty/<specialty_id>/doctors', TenantStaffDoctorsBySpecialityView.as_view()),
    path('v1/tenant/<pk>/staff/doctors', TenantStaffDoctorsView.as_view()),
]
