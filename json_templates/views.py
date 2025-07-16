from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import JsonTemplate, TemplateUsage
from .serializers import JsonTemplateSerializer, TemplateUsageSerializer, JsonTemplateListSerializer
import json
from django.db import models

class IsOwnerOrReadOnly(permissions.BasePermission):
    """템플릿 소유자만 수정/삭제 가능, 읽기는 모두 가능"""
    
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 쓰기 권한은 템플릿 소유자에게만 허용
        return obj.user == request.user

class JsonTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = JsonTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        # 자신의 템플릿과 공개된 템플릿만 조회 가능
        return JsonTemplate.objects.filter(
            models.Q(user=user) | models.Q(is_public=True)
        ).distinct()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JsonTemplateListSerializer
        return JsonTemplateSerializer
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """템플릿을 사용하여 더미 JSON 데이터 생성"""
        template = self.get_object()
        count = request.data.get('count', 1)
        
        # 생성할 개수 제한 (1-100개)
        count = max(1, min(100, int(count)))
        
        try:
            # 더미 데이터 생성
            dummy_data = template.generate_dummy_data(count)
            
            # 사용 기록 저장
            TemplateUsage.objects.create(
                template=template,
                user=request.user,
                generated_count=count
            )
            
            return Response({
                'template_id': template.id,
                'template_name': template.name,
                'generated_count': count,
                'data': dummy_data
            })
            
        except Exception as e:
            return Response({
                'error': f'더미 데이터 생성 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """템플릿 미리보기 (1개 샘플 생성)"""
        template = self.get_object()
        
        try:
            dummy_data = template.generate_dummy_data(1)
            return Response({
                'template_id': template.id,
                'template_name': template.name,
                'preview_data': dummy_data
            })
        except Exception as e:
            return Response({
                'error': f'미리보기 생성 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_templates(self, request):
        """내가 만든 템플릿만 조회"""
        templates = JsonTemplate.objects.filter(user=request.user)
        serializer = JsonTemplateListSerializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def public_templates(self, request):
        """공개된 템플릿만 조회"""
        templates = JsonTemplate.objects.filter(is_public=True)
        serializer = JsonTemplateListSerializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def validate_structure(self, request, pk=None):
        """템플릿 구조 유효성 검사"""
        template = self.get_object()
        
        try:
            # 템플릿 구조가 유효한 JSON인지 확인
            structure = template.template_structure
            
            # 실제로 더미 데이터를 생성해보아서 구조가 올바른지 테스트
            test_data = template.generate_dummy_data(1)
            
            return Response({
                'valid': True,
                'message': '템플릿 구조가 유효합니다.',
                'sample_output': test_data
            })
            
        except Exception as e:
            return Response({
                'valid': False,
                'error': f'템플릿 구조 오류: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

class TemplateUsageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TemplateUsageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return TemplateUsage.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def by_template(self, request):
        """템플릿별 사용 통계"""
        template_id = request.query_params.get('template_id')
        if template_id:
            usages = TemplateUsage.objects.filter(
                user=request.user,
                template_id=template_id
            )
        else:
            usages = TemplateUsage.objects.filter(user=request.user)
        
        serializer = self.get_serializer(usages, many=True)
        return Response(serializer.data)
