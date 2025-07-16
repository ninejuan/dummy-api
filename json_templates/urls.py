from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JsonTemplateViewSet, TemplateUsageViewSet

router = DefaultRouter()
router.register(r'templates', JsonTemplateViewSet, basename='jsontemplate')
router.register(r'usages', TemplateUsageViewSet, basename='templateusage')

urlpatterns = [
    path('', include(router.urls)),
] 