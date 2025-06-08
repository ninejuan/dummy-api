from django.db import models

class TextCategories(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.category_name

class Texts(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]  # Return the first 50 characters of the text for display
    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"
        ordering = ['-created_at']

class TCPeering(models.Model):
    text = models.ForeignKey(Texts, on_delete=models.CASCADE, related_name='peering_texts')
    category = models.ForeignKey(TextCategories, on_delete=models.CASCADE, related_name='peering_categories')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.text} - {self.category}"
    
    class Meta:
        verbose_name = "TCPeering"
        verbose_name_plural = "TCPeerings"
        ordering = ['-created_at']

def to_dict(self):
    return {
        'id': self.id,
        'text': self.text,
        'category_id': self.category.id if self.category else None
    }
Texts.to_dict = to_dict
def category_to_dict(self):
    return {
        'id': self.id,
        'name': self.name
    }
TextCategories.to_dict = category_to_dict
def link_to_dict(self):
    return {
        'id': self.id,
        'source': self.source,
        'target': self.target
    }
TCPeering.to_dict = link_to_dict