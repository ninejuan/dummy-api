from django.db import models
from django.utils import timezone

class TextCategories(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
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
        verbose_name = "Text Category"
        verbose_name_plural = "Text Categories"
        ordering = ['-created_at']

class Texts(models.Model):
    text = models.TextField()
    category = models.ForeignKey(TextCategories, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:50]

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'category': {
                'id': self.category.id,
                'category_name': self.category.category_name,
                'description': self.category.description
            } if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"
        ordering = ['-created_at']