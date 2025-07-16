from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodeCategoryViewSet, CodeSampleViewSet

router = DefaultRouter()
router.register(r'categories', CodeCategoryViewSet)
router.register(r'samples', CodeSampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 