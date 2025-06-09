from django.db import models
from django.utils import timezone

class ImageCategory(models.Model):
    category_name = models.CharField(max_length=100, default='default category')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category_name

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        db_table = 'image_categories'
        ordering = ['-created_at']
        verbose_name = '이미지 카테고리'
        verbose_name_plural = '이미지 카테고리'

class Images(models.Model):
    imageUrl = models.TextField(verbose_name="Image URL")
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.imageUrl

    def to_dict(self):
        return {
            'id': self.id,
            'imageUrl': self.imageUrl,
            'category': {
                'id': self.category.id,
                'category_name': self.category.category_name,
                'description': self.category.description
            } if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-created_at']
