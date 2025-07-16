from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class JsonCategory(models.Model):
    category_name = models.CharField(max_length=100, default='default category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category_name

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category_name,
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_jsons')
    is_approved = models.BooleanField(default=True, help_text="검열 통과 여부")
    is_flagged = models.BooleanField(default=False, help_text="욕설/금지어 포함 여부")
    flagged_reason = models.TextField(blank=True, null=True, help_text="검열 사유")
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
            'user': {
                'id': self.user.id,
                'username': self.user.username
            } if self.user else None,
            'is_approved': self.is_approved,
            'is_flagged': self.is_flagged,
            'flagged_reason': self.flagged_reason,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "JSON"
        verbose_name_plural = "JSONs"
        ordering = ['-created_at']

class JsonBannedWords(models.Model):
    """JSON용 금지어 관리"""
    word = models.CharField(max_length=100, unique=True)
    reason = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "JSON Banned Word"
        verbose_name_plural = "JSON Banned Words"
        ordering = ['word']
    
    def __str__(self):
        return self.word
