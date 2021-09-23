from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include  # add this
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

# Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Citas Medicas API",
        default_version='v1',
        description="API citas medicas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="demo@docu.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes= [permissions.AllowAny,]
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("", include("authentication.urls")),  # Auth routes - login / register
    # API V1
    # url(r'^api/login/', obtain_auth_token, name='api_token_auth'),
    url(r'^api/', include("tenants.urls")),
    url(r'^api/', include("commons.urls")),
    url(r'^api/', include("accounts.urls")),
    url(r'^api/', include("payment_gateways.urls")),
    url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", include("app.urls")),  # UI Kits Html files
]
