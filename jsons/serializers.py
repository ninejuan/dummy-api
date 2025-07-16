from rest_framework import serializers
from .models import JsonCategory, Jsons, JsonBannedWords

class JsonCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonCategory
        fields = '__all__'

class JsonsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Jsons
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'is_flagged', 'flagged_reason', 'created_at', 'updated_at']

class JsonBannedWordsSerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    
    class Meta:
        model = JsonBannedWords
        fields = '__all__'
        read_only_fields = ['added_by', 'created_at'] 