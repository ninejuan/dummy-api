from rest_framework import serializers
from .models import JsonTemplate, TemplateUsage

class JsonTemplateSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JsonTemplate
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_usage_count(self, obj):
        return obj.usages.count()
    
    def create(self, validated_data):
        # 현재 로그인한 사용자를 템플릿 소유자로 설정
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TemplateUsageSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TemplateUsage
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class JsonTemplateListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JsonTemplate
        fields = ['id', 'name', 'description', 'user_username', 'is_public', 'created_at', 'usage_count']
    
    def get_usage_count(self, obj):
        return obj.usages.count() 