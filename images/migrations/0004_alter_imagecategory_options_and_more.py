# Generated by Django 5.2.2 on 2025-06-09 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20250609_0123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagecategory',
            options={'ordering': ['-created_at'], 'verbose_name': '이미지 카테고리', 'verbose_name_plural': '이미지 카테고리'},
        ),
        migrations.RemoveField(
            model_name='imagecategory',
            name='title',
        ),
        migrations.RemoveField(
            model_name='images',
            name='title',
        ),
        migrations.AddField(
            model_name='imagecategory',
            name='category_name',
            field=models.CharField(default='default category', max_length=100),
        ),
        migrations.AlterField(
            model_name='images',
            name='imageUrl',
            field=models.TextField(verbose_name='Image URL'),
        ),
        migrations.AlterModelTable(
            name='imagecategory',
            table='image_categories',
        ),
    ]
