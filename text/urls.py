from django.urls import path
from . import views

urlpatterns = [
    # 기존 기능들
    path('categories/<int:page>/<int:limit>/', views.get_all_categories, name='get_all_categories'),
    path('texts/<int:page>/<int:limit>/', views.get_all_texts, name='get_all_texts'),
    path('texts/category/<int:category_id>/<int:page>/<int:limit>/', views.get_texts_by_category, name='get_texts_by_category'),
    path('texts/id/<int:value_id>/', views.get_text_by_id, name='get_text_by_id'),
    path('categories/info/<str:category_name>/', views.get_category_info, name='get_category_info'),
    path('texts/random/', views.get_random_text, name='get_random_text'),
    
    # 사용자 참여형 기능들
    path('user/create/', views.create_user_text, name='create_user_text'),
    path('user/my-texts/<int:page>/<int:limit>/', views.get_my_texts, name='get_my_texts'),
    path('texts/approved/<int:page>/<int:limit>/', views.get_approved_texts, name='get_approved_texts'),
    
    # 금지어 관리
    path('banned-words/', views.get_banned_words, name='get_banned_words'),
    path('banned-words/add/', views.add_banned_word, name='add_banned_word'),
    path('banned-words/delete/<int:word_id>/', views.delete_banned_word, name='delete_banned_word'),
    
    # 검열 테스트
    path('test-censorship/', views.test_censorship, name='test_censorship'),
]