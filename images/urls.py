from django.urls import path
from . import views

urlpatterns = [
    path('all/categories/<str:page>/<str:limit>/', views.get_all_categories, name='get_all_categories'),
    path('all/images/<str:page>/<str:limit>/', views.get_all_images, name='get_all_images'),
    path('category/<str:category_name>/', views.get_category_by_name, name='get_category_info'),
    path('get/categoryid/<str:category_id>/<str:page>/<str:limit>/', views.get_images_by_category, name='get_images_by_category'),
    path('get/imageid/<str:image_id>/', views.get_image_by_id, name='get_image_by_id'),
    path('random/', views.get_random_image, name='get_random_image'),
]