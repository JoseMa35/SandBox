"""xiabel URL Configuration"""
from django.urls import path, include # new

from .views import (SpecialtyList, SpecialtyDoctorList, SpecialtyDetail, SpecialtyDoctorDetail, )

urlpatterns = [
    path('doctors/', SpecialtyDoctorList.as_view()),
    path('doctor/<int:pk>/', SpecialtyDoctorDetail.as_view()),
    path('specialties', SpecialtyList.as_view()),
    path('specialty/<int:pk>/', SpecialtyDetail.as_view()),
]
