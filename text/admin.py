from django.contrib import admin
from .models import TextCategories, Texts

@admin.register(TextCategories)
class TextCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at', 'updated_at')
    search_fields = ('category_name',)
    ordering = ('-created_at',)

@admin.register(Texts)
class TextsAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'updated_at')
    search_fields = ('text',)
    ordering = ('-created_at',)
