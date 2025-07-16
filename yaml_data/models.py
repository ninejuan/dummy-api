from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class YamlCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "YAML Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class YamlData(models.Model):
    category = models.ForeignKey(YamlCategory, on_delete=models.CASCADE, related_name='yaml_data')
    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=50, default='yaml')
    tags = models.JSONField(default=list, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_yaml_data')
    is_approved = models.BooleanField(default=True, help_text="검열 통과 여부")
    is_flagged = models.BooleanField(default=False, help_text="욕설/금지어 포함 여부")
    flagged_reason = models.TextField(blank=True, null=True, help_text="검열 사유")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "YAML Data"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class YamlBannedWords(models.Model):
    """YAML용 금지어 관리"""
    word = models.CharField(max_length=100, unique=True)
    reason = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "YAML Banned Word"
        verbose_name_plural = "YAML Banned Words"
        ordering = ['word']
    
    def __str__(self):
        return self.word
