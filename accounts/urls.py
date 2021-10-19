
from django.urls import path, include  # new

from accounts.views import ProfileView, ProfileListView

urlpatterns = [
    # path('v1/users/',  ()),
    path('v1/user/<pk>', ProfileView.as_view()),
    path('v1/user', ProfileListView.as_view()),
]