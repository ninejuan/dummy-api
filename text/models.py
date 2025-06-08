from django.db import models

class TextCategories(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(TextCategories, on_delete=models.CASCADE, related_name='texts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
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

class TCPeering(models.Model):
    text = models.ForeignKey(Texts, on_delete=models.CASCADE, related_name='peering_texts')
    category = models.ForeignKey(TextCategories, on_delete=models.CASCADE, related_name='peering_categories')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text} - {self.category}"

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text.to_dict() if self.text else None,
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "TCPeering"
        verbose_name_plural = "TCPeerings"
        ordering = ['-created_at']