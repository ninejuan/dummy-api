from django.urls import path
from . import views

urlpatterns = [
    # GET
    path('categories/', views.get_all_categories, name='get_all_categories'),
    path('values/', views.get_all_values, name='get_all_values'),
    path('links/', views.get_all_links, name='get_all_links'),
    path('categories/values/<str:category_id>/', views.get_values_by_category, name='get_values_by_category'),
    path('values/get/<str:value_id>/', views.get_value_by_id, name='get_value_by_id'),
    path('values/random/', views.get_random_value, name='get_random_value'),
    # POST
    path('categories/add/', views.add_category, name='add_category'),
    path('values/add/', views.add_value, name='add_value'),
    path('links/add/', views.add_link, name='add_link'),
    # PUT
    path('categories/update/<str:category_id>/', views.update_category, name='update_category'),
    path('values/update/<str:value_id>/', views.update_value, name='update_value'),
    # DELETE
    path('categories/delete/<str:category_id>/', views.delete_category, name='delete_category'),
    path('values/delete/<str:value_id>/', views.delete_value, name='delete_value'),
    path('links/delete/<str:link_id>/', views.delete_link, name='delete_link'),
]