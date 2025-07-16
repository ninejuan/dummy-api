from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import YamlCategory, YamlData
from .serializers import YamlCategorySerializer, YamlDataSerializer
import yaml
import json

class YamlCategoryViewSet(viewsets.ModelViewSet):
    queryset = YamlCategory.objects.all()
    serializer_class = YamlCategorySerializer
    
    @action(detail=True, methods=['get'])
    def yaml_data(self, request, pk=None):
        category = self.get_object()
        yaml_data = category.yaml_data.all()
        serializer = YamlDataSerializer(yaml_data, many=True)
        return Response(serializer.data)

class YamlDataViewSet(viewsets.ModelViewSet):
    queryset = YamlData.objects.all()
    serializer_class = YamlDataSerializer
    
    @action(detail=True, methods=['get'])
    def as_json(self, request, pk=None):
        yaml_obj = self.get_object()
        try:
            # YAML을 JSON으로 변환
            yaml_content = yaml.safe_load(yaml_obj.content)
            return Response({
                'id': yaml_obj.id,
                'title': yaml_obj.title,
                'category': yaml_obj.category.name,
                'yaml_content': yaml_obj.content,
                'json_content': yaml_content,
                'tags': yaml_obj.tags
            })
        except yaml.YAMLError as e:
            return Response({'error': f'YAML 파싱 오류: {str(e)}'}, status=400)
    
    @action(detail=False, methods=['post'])
    def validate_yaml(self, request):
        content = request.data.get('content', '')
        try:
            yaml.safe_load(content)
            return Response({'valid': True, 'message': '유효한 YAML입니다.'})
        except yaml.YAMLError as e:
            return Response({'valid': False, 'error': str(e)}, status=400)
