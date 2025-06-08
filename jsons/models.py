from django.db import models

class JsonCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="JSON Category")
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
        verbose_name = "JSON Category"
        verbose_name_plural = "JSON Categories"
        ordering = ['-created_at']

    def get_jsons(self):
        return self.jsons.all()

    def get_json_count(self):
        return self.jsons.count()

    def get_first_json(self):
        return self.jsons.first()

class Jsons(models.Model):
    title = models.CharField(max_length=100, verbose_name="JSON Title")
    json_data = models.JSONField(verbose_name="JSON Data")
    category = models.ForeignKey(JsonCategory, on_delete=models.CASCADE, related_name='jsons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'json_data': self.json_data,
            'category': {
                'id': self.category.id,
                'title': self.category.title,
                'description': self.category.description
            } if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "JSON"
        verbose_name_plural = "JSONs"
        ordering = ['-created_at']

class JCPeering(models.Model):
    json_data = models.ForeignKey(Jsons, on_delete=models.CASCADE, related_name='jc_peering', verbose_name="JSON Data")
    category = models.ForeignKey(JsonCategory, on_delete=models.CASCADE, related_name='jc_peering_category', verbose_name="JSON Category")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.json_data.title} - {self.category.title}"

    def to_dict(self):
        return {
            'id': self.id,
            'json_data': self.json_data.to_dict() if self.json_data else None,
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    class Meta:
        verbose_name = "JC Peering"
        verbose_name_plural = "JC Peerings"
        ordering = ['-created_at']

    def get_json(self):
        return self.json_data.json_data