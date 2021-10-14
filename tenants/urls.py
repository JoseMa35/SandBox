""" URL Configuration"""
from django.urls import path, include  # new

from commons.integrations.mercadopago import pagoefectivo
from tenants.views import TenantListView, TenantDetailView, TenantStaffDoctorDetailBySpecialityView, BookingFileView
from tenants.views import TenantStaffView, TenantStaffSpecialitiesView
from tenants.views import TenantStaffDoctorsBySpecialityView, TenantStaffDoctorsView
from tenants.views import BookingView
from commons.integrations import gcalendar

urlpatterns = [
    path('v1/tenants/',TenantListView.as_view()),
    path('v1/tenant/<pk>',TenantDetailView.as_view()),
    path('v1/tenant/<pk>/staff',TenantStaffView.as_view()),
    path('v1/tenant/<pk>/staff/specialties',TenantStaffSpecialitiesView.as_view()),
    path('v1/tenant/<pk>/staff/specialty/<specialty_id>/doctors',TenantStaffDoctorsBySpecialityView.as_view()),
    path('v1/tenant/<pk>/staff/specialty/<specialty_id>/doctor/<doctor_id>',TenantStaffDoctorDetailBySpecialityView.as_view()),
    path('v1/tenant/<pk>/staff/doctors', TenantStaffDoctorsView.as_view()),
    path('v1/doctor/<pk>/schedule', gcalendar.free_time),
    path('v1/booking/files/', BookingFileView.as_view()),
    path('v1/tenant/<pk>/staff/booking', BookingView.as_view()),
     # path('v1/booking/file/<pk>', BookingFileView.as_view()),

    # Payment
    path('v1/mercadopago/payment', pagoefectivo.available_payment_list),
    path('v1/mercadopago/payment/pagoefectivo', pagoefectivo.available_payment),
    path('v1/mercadopago/transaction/pagoefectivo', pagoefectivo.transaction_payment),

    # Create event
    path('v1/gmap/create/event', gcalendar.insert_event)

]
