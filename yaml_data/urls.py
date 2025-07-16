from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YamlCategoryViewSet, YamlDataViewSet

router = DefaultRouter()
router.register(r'categories', YamlCategoryViewSet)
router.register(r'data', YamlDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 