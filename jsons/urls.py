from django.urls import path
from . import views

urlpatterns = [
    path('all/categories/<str:page>/<str:limit>/', views.get_all_categories, name='get_all_categories'),
    path('all/jsons/<str:page>/<str:limit>/', views.get_all_jsons, name='get_all_jsons'),
    path('category/<str:category_name>/', views.get_category_info, name='get_category_info'), # 수정필요
    path('get/categoryid/<str:category_id>/<str:page>/<str:limit>/', views.get_jsons_by_category, name='get_jsons_by_category'),
    path('get/jsonid/<str:json_id>/', views.get_json_by_id, name='get_json_by_id'),
    path('random/', views.get_random_json, name='get_random_json'),
]