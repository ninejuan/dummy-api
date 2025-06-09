from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.get_all_categories, name='get_all_categories'),
    path('values/', views.get_all_values, name='get_all_values'),
    path('categories/values/<str:category_id>/', views.get_values_by_category, name='get_values_by_category'),
    path('values/get/<str:value_id>/', views.get_value_by_id, name='get_value_by_id'),
    path('values/random/', views.get_random_value, name='get_random_value'),
]