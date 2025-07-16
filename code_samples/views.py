from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CodeCategory, CodeSample
from .serializers import CodeCategorySerializer, CodeSampleSerializer
import ast
import re

class CodeCategoryViewSet(viewsets.ModelViewSet):
    queryset = CodeCategory.objects.all()
    serializer_class = CodeCategorySerializer
    
    @action(detail=True, methods=['get'])
    def code_samples(self, request, pk=None):
        category = self.get_object()
        code_samples = category.code_samples.all()
        serializer = CodeSampleSerializer(code_samples, many=True)
        return Response(serializer.data)

class CodeSampleViewSet(viewsets.ModelViewSet):
    queryset = CodeSample.objects.all()
    serializer_class = CodeSampleSerializer
    
    @action(detail=True, methods=['get'])
    def syntax_check(self, request, pk=None):
        code_sample = self.get_object()
        language = code_sample.language.lower()
        
        if language == 'python':
            try:
                ast.parse(code_sample.code)
                return Response({
                    'valid': True,
                    'message': '유효한 Python 코드입니다.'
                })
            except SyntaxError as e:
                return Response({
                    'valid': False,
                    'error': f'구문 오류: {str(e)}',
                    'line': e.lineno
                }, status=400)
        else:
            return Response({
                'valid': None,
                'message': f'{language} 언어의 구문 검사는 지원되지 않습니다.'
            })
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        code_sample = self.get_object()
        code = code_sample.code
        
        stats = {
            'total_lines': len(code.split('\n')),
            'code_lines': len([line for line in code.split('\n') if line.strip()]),
            'comment_lines': len([line for line in code.split('\n') if line.strip().startswith('#')]),
            'character_count': len(code),
            'word_count': len(code.split()),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        difficulty = request.query_params.get('difficulty', 'beginner')
        code_samples = self.queryset.filter(difficulty=difficulty)
        serializer = self.get_serializer(code_samples, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_language(self, request):
        language = request.query_params.get('language', 'python')
        code_samples = self.queryset.filter(language__iexact=language)
        serializer = self.get_serializer(code_samples, many=True)
        return Response(serializer.data)
