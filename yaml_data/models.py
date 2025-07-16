from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "YAML Data"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
