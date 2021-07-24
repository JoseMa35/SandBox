"""xiabel URL Configuration"""
from django.conf.urls import url

from .views import (GenderListView, GenderDetailView, DocumentTypeListView, )

urlpatterns = [
    url(r'^genders/$', GenderListView.as_view(), name='genders_list'),
    url(r'^documents/$', DocumentTypeListView.as_view(), name='document_list'),
]
