
from django.urls import path, include  # new

from accounts.views import UserProfileView

urlpatterns = [
    # path('v1/users/',  ()),
    path('v1/user/<pk>', UserProfileView.as_view()),
]