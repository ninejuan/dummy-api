from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YamlCategoryViewSet, YamlDataViewSet, YamlBannedWordsViewSet

router = DefaultRouter()
router.register(r'categories', YamlCategoryViewSet)
router.register(r'data', YamlDataViewSet, basename='yamldata')
router.register(r'banned-words', YamlBannedWordsViewSet, basename='yamlbannedwords')

urlpatterns = [
    path('', include(router.urls)),
] 