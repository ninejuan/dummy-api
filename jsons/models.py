from django.db import models
from django.utils import timezone

class JsonCategory(models.Model):
    category_name = models.CharField(max_length=100, default='default category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category_name

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "JSON Category"
        verbose_name_plural = "JSON Categories"
        ordering = ['-created_at']

class Jsons(models.Model):
    title = models.CharField(max_length=100)
    jsonData = models.JSONField(verbose_name="JSON Data")
    category = models.ForeignKey(JsonCategory, on_delete=models.CASCADE, related_name='jsons', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'jsonData': self.jsonData,
            'category': {
                'id': self.category.id,
                'category_name': self.category.category_name,
            } if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "JSON"
        verbose_name_plural = "JSONs"
        ordering = ['-created_at']
