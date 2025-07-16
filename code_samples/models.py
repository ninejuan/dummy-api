from django.db import models

# Create your models here.

class CodeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, default='python')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Code Categories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.language})"

class CodeSample(models.Model):
    category = models.ForeignKey(CodeCategory, on_delete=models.CASCADE, related_name='code_samples')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', '초급'),
        ('intermediate', '중급'),
        ('advanced', '고급')
    ], default='beginner')
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Code Samples"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
