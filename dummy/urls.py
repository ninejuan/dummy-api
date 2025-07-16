from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dummy API",
        default_version="v1",
        description="Dummy API documentation",
        contact=openapi.Contact(email="contact+dummy@juany.kr"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('text/', include('text.urls')),
    path('images/', include('images.urls')),
    path('jsons/', include('jsons.urls')),
    path('accounts/', include('accounts.urls')),
    path('yaml/', include('yaml_data.urls')),
    path('code/', include('code_samples.urls')),
    path('json-templates/', include('json_templates.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
