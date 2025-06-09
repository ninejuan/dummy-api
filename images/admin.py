from django.contrib import admin
from .models import ImageCategory, Images

@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description', 'created_at', 'updated_at')
    search_fields = ('category_name',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'imageUrl', 'category', 'created_at', 'updated_at')
    search_fields = ('imageUrl',)
    ordering = ('-created_at',)
    list_filter = ('created_at', 'category')