from django.db import models

class ImageCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Image Category")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class ICPeering(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE, related_name='ic_peering', verbose_name="Image")
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='ic_peering_category', verbose_name="Image Category")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.image.title} - {self.category.title}"

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image.to_dict() if self.image else None,
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "IC Peering"
        verbose_name_plural = "IC Peerings"
        ordering = ['-created_at']