from django.contrib import admin
from .models import JsonCategory, Jsons

@admin.register(JsonCategory)
class JsonCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')
    search_fields = ('category_name',)
    ordering = ('-created_at',)

@admin.register(Jsons)
class JsonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'jsonData', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('jsonData', 'category__category_name')
    ordering = ('-created_at',)