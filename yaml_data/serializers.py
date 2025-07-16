from rest_framework import serializers
from .models import YamlCategory, YamlData

class YamlCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = YamlCategory
        fields = '__all__'

class YamlDataSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = YamlData
        fields = '__all__' 