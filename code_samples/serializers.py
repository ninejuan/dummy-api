from rest_framework import serializers
from .models import CodeCategory, CodeSample

class CodeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeCategory
        fields = '__all__'

class CodeSampleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    language_name = serializers.CharField(source='category.language', read_only=True)
    
    class Meta:
        model = CodeSample
        fields = '__all__' 