"""xiabel URL Configuration"""

from django.urls import path
from .views import (GenderListView, GenderDetailView, DocumentTypeListView, )

urlpatterns = [
    path('v1/common/genders', GenderListView.as_view()),
    path('v1/common/documents', DocumentTypeListView.as_view()),
]
