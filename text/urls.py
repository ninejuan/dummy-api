from django.urls import path
from . import views

urlpatterns = [
    path('all/categories/<str:page>/<str:limit>/', views.get_all_categories, name='get_all_categories'),
    path('all/texts/<str:page>/<str:limit>/', views.get_all_texts, name='get_all_texts'),
    path('category/<str:category_name>/', views.get_category_info, name='get_category_info'),
    path('get/categoryid/<str:category_id>/<str:page>/<str:limit>/', views.get_texts_by_category, name='get_texts_by_category'),
    path('get/textid/<str:value_id>/', views.get_text_by_id, name='get_text_by_id'),
    path('random/', views.get_random_text, name='get_random_text'),
]