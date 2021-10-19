from django.urls import path
from . import views

urlpatterns = [
    path(
        'v1/mails/confirmation/',
        views.ConfirmationSendEmailApiView.as_view(),
    )
]