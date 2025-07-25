from rest_framework import serializers
from .models import YamlCategory, YamlData, YamlBannedWords

class YamlCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = YamlCategory
        fields = '__all__'

class YamlDataSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = YamlData
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'is_flagged', 'flagged_reason', 'created_at', 'updated_at']

class YamlBannedWordsSerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    
    class Meta:
        model = YamlBannedWords
        fields = '__all__'
        read_only_fields = ['added_by', 'created_at'] 