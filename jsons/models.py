from django.db import models

class Jsons(models.Model):
    title = models.CharField(max_length=100, verbose_name="JSON Title")
    json_data = models.JSONField(verbose_name="JSON Data")

    def __str__(self):
        return self.title

class JsonCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="JSON Category")
    jsons = models.ManyToManyField(Jsons, related_name='categories', verbose_name="JSONs")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "JSON Category"
        verbose_name_plural = "JSON Categories"
        ordering = ['title']

    def get_jsons(self):
        return self.jsons.all()

    def get_json_count(self):
        return self.jsons.count()

    def get_first_json(self):
        return self.jsons.first()
        
class JCPeering(models.Model):
    json_data = models.ForeignKey(Jsons, on_delete=models.CASCADE, related_name='jc_peering', verbose_name="JSON Data")
    category = models.ForeignKey(JsonCategory, on_delete=models.CASCADE, related_name='jc_peering_category', verbose_name="JSON Category")
    def __str__(self):
        return f"{self.json_data.title} - {self.category.title}"
    class Meta:
        verbose_name = "JC Peering"
        verbose_name_plural = "JC Peerings"
        ordering = ['json_data__title']
    def get_json(self):
        return self.json_data.json_data