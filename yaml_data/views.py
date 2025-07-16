from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import YamlCategory, YamlData, YamlBannedWords
from .serializers import YamlCategorySerializer, YamlDataSerializer, YamlBannedWordsSerializer
import yaml
import json
import korcen

def check_yaml_profanity(yaml_content):
    """YAML 내용의 욕설 및 금지어 검사"""
    try:
        # YAML을 파싱하여 문자열 값들을 추출
        yaml_data = yaml.safe_load(yaml_content)
        
        def check_text_recursively(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        profanity_result = check_profanity(value)
                        if not profanity_result['is_clean']:
                            return profanity_result
                    elif isinstance(value, (dict, list)):
                        result = check_text_recursively(value)
                        if result and not result['is_clean']:
                            return result
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, str):
                        profanity_result = check_profanity(item)
                        if not profanity_result['is_clean']:
                            return profanity_result
                    elif isinstance(item, (dict, list)):
                        result = check_text_recursively(item)
                        if result and not result['is_clean']:
                            return result
            return {'is_clean': True, 'is_profane': False, 'found_banned_words': []}
        
        return check_text_recursively(yaml_data)
    except yaml.YAMLError:
        # YAML 파싱 실패 시 원본 텍스트로 검사
        return check_profanity(yaml_content)

def check_profanity(text):
    """욕설 및 금지어 검사"""
    # korcen으로 욕설 검사
    profanity_checker = korcen.ProfanityChecker()
    is_profane = profanity_checker.check(text)
    
    # 금지어 검사
    banned_words = YamlBannedWords.objects.all()
    found_banned_words = []
    
    for banned_word in banned_words:
        if banned_word.word.lower() in text.lower():
            found_banned_words.append(banned_word.word)
    
    return {
        'is_profane': is_profane,
        'found_banned_words': found_banned_words,
        'is_clean': not is_profane and len(found_banned_words) == 0
    }

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
    
    def get_queryset(self):
        # 승인된 YAML만 조회
        return YamlData.objects.filter(is_approved=True)
    
    @action(detail=False, methods=['post'])
    def create_user_yaml(self, request):
        """사용자가 YAML 등록 (로그인 필요)"""
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다'}, status=401)
        try:
            title = request.data.get('title', '').strip()
            content = request.data.get('content', '').strip()
            category_id = request.data.get('category_id')
            language = request.data.get('language', 'yaml')
            tags = request.data.get('tags', [])
            
            if not title or not content:
                return Response({'error': '제목과 YAML 내용이 필요합니다'}, status=400)
            
            # YAML 내용 검열
            profanity_result = check_yaml_profanity(content)
            
            if not profanity_result['is_clean']:
                # 검열 실패 시에도 저장하되 승인되지 않은 상태로
                yaml_obj = YamlData.objects.create(
                    title=title,
                    content=content,
                    category_id=category_id,
                    language=language,
                    tags=tags,
                    user=request.user,
                    is_approved=False,
                    is_flagged=True,
                    flagged_reason=f"욕설 포함: {profanity_result['is_profane']}, 금지어: {', '.join(profanity_result['found_banned_words'])}"
                )
                
                return Response({
                    'error': '욕설이나 금지어가 포함되어 승인되지 않았습니다',
                    'flagged_reason': yaml_obj.flagged_reason,
                    'yaml_id': yaml_obj.id
                }, status=403)
            
            # 검열 통과 시 정상 저장
            yaml_obj = YamlData.objects.create(
                title=title,
                content=content,
                category_id=category_id,
                language=language,
                tags=tags,
                user=request.user,
                is_approved=True,
                is_flagged=False
            )
            
            return Response({
                'message': 'YAML이 성공적으로 등록되었습니다',
                'yaml': yaml_obj.to_dict()
            }, status=201)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['get'])
    def my_yaml_data(self, request):
        """내가 등록한 YAML 조회"""
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다'}, status=401)
        my_yaml_data = YamlData.objects.filter(user=request.user)
        serializer = self.get_serializer(my_yaml_data, many=True)
        return Response(serializer.data)
    
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
                'user': yaml_obj.user.username if yaml_obj.user else None,
                'tags': yaml_obj.tags
            })
        except yaml.YAMLError as e:
            return Response({'error': f'YAML 파싱 오류: {str(e)}'}, status=400)
    
    @action(detail=False, methods=['post'])
    def validate_yaml(self, request):
        """YAML 유효성 검사"""
        content = request.data.get('content', '')
        if not content:
            return Response({'error': 'YAML 내용이 필요합니다'}, status=400)
        
        try:
            # YAML 형식 검사
            yaml.safe_load(content)
            
            # 검열 검사
            profanity_result = check_yaml_profanity(content)
            
            return Response({
                'valid': True,
                'is_clean': profanity_result['is_clean'],
                'message': '유효한 YAML입니다.' if profanity_result['is_clean'] else '욕설이나 금지어가 포함되어 있습니다.'
            })
        except yaml.YAMLError as e:
            return Response({'valid': False, 'error': f'잘못된 YAML 형식입니다: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'valid': False, 'error': str(e)}, status=400)

class YamlBannedWordsViewSet(viewsets.ModelViewSet):
    queryset = YamlBannedWords.objects.all()
    serializer_class = YamlBannedWordsSerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        word = request.data.get('word', '').strip()
        reason = request.data.get('reason', '')
        
        if not word:
            return Response({'error': '금지어가 필요합니다'}, status=400)
        
        if YamlBannedWords.objects.filter(word=word).exists():
            return Response({'error': '이미 존재하는 금지어입니다'}, status=400)
        
        banned_word = YamlBannedWords.objects.create(
            word=word,
            reason=reason,
            added_by=request.user
        )
        
        return Response({
            'message': '금지어가 추가되었습니다',
            'word': word,
            'reason': reason
        }, status=201)
