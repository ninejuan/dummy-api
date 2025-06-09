from django.db import models
from django.utils import timezone

class ImageCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Image Category")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "Image Category"
        verbose_name_plural = "Image Categories"
        ordering = ['-created_at']

class Images(models.Model):
    title = models.CharField(max_length=100, verbose_name="Image Title")
    imageUrl = models.ImageField(upload_to='images/', verbose_name="Image URL")
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'imageUrl': self.imageUrl.url if self.imageUrl else None,
            'category': {
                'id': self.category.id,
                'title': self.category.title,
                'description': self.category.description
            } if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-created_at']
