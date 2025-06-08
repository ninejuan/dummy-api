from django.db import models

class Images(models.Model):
    title = models.CharField(max_length=100, verbose_name="Image Title")
    imageUrl = models.ImageField(verbose_name="image url")

    def __str__(self):
        return self.imageUrl

class ImageCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Image Category")
    images = models.ManyToManyField(Images, related_name='categories', verbose_name="Images")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Image Category"
        verbose_name_plural = "Image Categories"
    ordering = ['title']
    def get_images(self):
        return self.images.all()
    def get_image_count(self):
        return self.images.count()
    def get_first_image(self):
        return self.images.first()

class ICPeering(models.Model):
    imageUrl = models.ImageField(verbose_name="image url")
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='ic_peering', verbose_name="Image Category")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "IC Peering"
        verbose_name_plural = "IC Peerings"
    ordering = ['title']
    
    def get_image(self):
        return self.imageUrl