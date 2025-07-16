from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import JsonCategory, Jsons, JsonBannedWords
from django.views.decorators.http import require_http_methods
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import JsonCategorySerializer, JsonsSerializer, JsonBannedWordsSerializer
import random
import korcen

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 JSON 카테고리 조회 (페이지네이션)",
    responses={
        200: openapi.Response(description="카테고리 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 카테고리 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='카테고리 ID'),
                            'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 이름'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="카테고리가 없음"),
        400: openapi.Response(description="잘못된 페이지 번호 또는 한 페이지당 항목 수")
    },
)
@require_http_methods(["GET"])
def get_all_categories(request, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        categories = JsonCategory.objects.all()
        if not categories.exists():
            return JsonResponse({'error': '카테고리가 없습니다'}, status=404)
            
        total_count = categories.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_categories = categories[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'categories': [category.to_dict() for category in paginated_categories]
        }
        
        return JsonResponse(response_data)
    except ValueError:
        return JsonResponse({'error': '잘못된 페이지 번호 또는 한 페이지당 항목 수입니다'}, status=400)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 JSON 조회 (페이지네이션)",
    responses={
        200: openapi.Response(description="JSON 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 JSON 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'jsons': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='JSON ID'),
                            'json_data': openapi.Schema(type=openapi.TYPE_OBJECT, description='JSON 데이터'),
                            'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="JSON이 없음"),
        400: openapi.Response(description="잘못된 페이지 번호 또는 한 페이지당 항목 수")
    },
)
@require_http_methods(["GET"])
def get_all_jsons(request, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        jsons = Jsons.objects.all()
        if not jsons.exists():
            return JsonResponse({'error': 'JSON이 없습니다'}, status=404)
            
        total_count = jsons.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_jsons = jsons[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'jsons': [json.to_dict() for json in paginated_jsons]
        }
        
        return JsonResponse(response_data)
    except ValueError:
        return JsonResponse({'error': '잘못된 페이지 번호 또는 한 페이지당 항목 수입니다'}, status=400)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="카테고리 정보 조회",
    manual_parameters=[
        openapi.Parameter('category_name', openapi.IN_QUERY, description="카테고리 이름", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response(description="카테고리 정보 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='카테고리 ID'),
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 이름'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="카테고리를 찾을 수 없음")
    },
)
@require_http_methods(["GET"])
def get_category_info(request, category_name):
    if not category_name:
        return JsonResponse({'error': '카테고리 이름이 필요합니다'}, status=400)
    try:
        category = JsonCategory.objects.get(category_name=category_name)
    except JsonCategory.DoesNotExist:
        return JsonResponse({'error': '해당 카테고리를 찾을 수 없습니다'}, status=404)
    return JsonResponse(category.to_dict())

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="카테고리별 JSON 조회 (페이지네이션)",
    responses={
        200: openapi.Response(description="JSON 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 JSON 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'jsons': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='JSON ID'),
                            'title': openapi.Schema(type=openapi.TYPE_STRING, description='JSON 제목'),
                            'jsonData': openapi.Schema(type=openapi.TYPE_OBJECT, description='JSON 데이터'),
                            'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="JSON이 없음"),
        400: openapi.Response(description="잘못된 페이지 번호 또는 한 페이지당 항목 수")
    },
)
@require_http_methods(["GET"])
def get_jsons_by_category(request, category_id, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        jsons = Jsons.objects.filter(category_id=category_id)
        if not jsons.exists():
            return JsonResponse({'error': '해당 카테고리의 JSON이 없습니다'}, status=404)
            
        total_count = jsons.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_jsons = jsons[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'jsons': [json.to_dict() for json in paginated_jsons]
        }
        
        return JsonResponse(response_data)
    except ValueError:
        return JsonResponse({'error': '잘못된 페이지 번호 또는 한 페이지당 항목 수입니다'}, status=400)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="ID로 JSON 조회",
    manual_parameters=[
        openapi.Parameter('json_id', openapi.IN_QUERY, description="JSON ID", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response(description="JSON 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='JSON ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='JSON 제목'),
                'jsonData': openapi.Schema(type=openapi.TYPE_OBJECT, description='JSON 데이터'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="JSON을 찾을 수 없음")
    },
)
@require_http_methods(["GET"])
def get_json_by_id(request, json_id):
    if not json_id:
        return JsonResponse({'error': 'JSON ID가 필요합니다'}, status=400)
    
    try:
        json_data = Jsons.objects.get(id=json_id)
    except Jsons.DoesNotExist:
        return JsonResponse({'error': '해당 JSON을 찾을 수 없습니다'}, status=404)
    
    return JsonResponse(json_data.to_dict())

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="랜덤 JSON 조회",
    responses={
        200: openapi.Response(description="JSON 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='JSON ID'),
                'json_data': openapi.Schema(type=openapi.TYPE_OBJECT, description='JSON 데이터'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="JSON이 없음")
    },
)
@require_http_methods(["GET"])
def get_random_json(request):
    import random
    jsons = Jsons.objects.all()
    if not jsons.exists():
        return JsonResponse({'error': 'JSON이 없습니다'}, status=404)
    
    random_json = random.choice(jsons)
    return JsonResponse(random_json.to_dict())

def check_json_profanity(json_data):
    """JSON 데이터 내의 욕설 및 금지어 검사"""
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

    return check_text_recursively(json_data)

def check_profanity(text):
    """욕설 및 금지어 검사"""
    # korcen으로 욕설 검사
    profanity_checker = korcen.ProfanityChecker()
    is_profane = profanity_checker.check(text)
    
    # 금지어 검사
    banned_words = JsonBannedWords.objects.all()
    found_banned_words = []
    
    for banned_word in banned_words:
        if banned_word.word.lower() in text.lower():
            found_banned_words.append(banned_word.word)
    
    return {
        'is_profane': is_profane,
        'found_banned_words': found_banned_words,
        'is_clean': not is_profane and len(found_banned_words) == 0
    }

class JsonCategoryViewSet(viewsets.ModelViewSet):
    queryset = JsonCategory.objects.all()
    serializer_class = JsonCategorySerializer
    
    @action(detail=True, methods=['get'])
    def jsons(self, request, pk=None):
        category = self.get_object()
        jsons_data = category.jsons.all()
        serializer = JsonsSerializer(jsons_data, many=True)
        return Response(serializer.data)

class JsonsViewSet(viewsets.ModelViewSet):
    queryset = Jsons.objects.all()
    serializer_class = JsonsSerializer
    
    def get_queryset(self):
        # 승인된 JSON만 조회
        return Jsons.objects.filter(is_approved=True)
    
    @action(detail=False, methods=['post'])
    def create_user_json(self, request):
        """사용자가 JSON 등록 (로그인 필요)"""
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다'}, status=401)
            
        try:
            title = request.data.get('title', '').strip()
            json_data = request.data.get('jsonData')
            category_id = request.data.get('category_id')
            
            if not title or not json_data:
                return Response({'error': '제목과 JSON 데이터가 필요합니다'}, status=400)
            
            # JSON 데이터 검열
            profanity_result = check_json_profanity(json_data)
            
            if not profanity_result['is_clean']:
                # 검열 실패 시에도 저장하되 승인되지 않은 상태로
                json_obj = Jsons.objects.create(
                    title=title,
                    jsonData=json_data,
                    category_id=category_id,
                    user=request.user,
                    is_approved=False,
                    is_flagged=True,
                    flagged_reason=f"욕설 포함: {profanity_result['is_profane']}, 금지어: {', '.join(profanity_result['found_banned_words'])}"
                )
                
                return Response({
                    'error': '욕설이나 금지어가 포함되어 승인되지 않았습니다',
                    'flagged_reason': json_obj.flagged_reason,
                    'json_id': json_obj.id
                }, status=403)
            
            # 검열 통과 시 정상 저장
            json_obj = Jsons.objects.create(
                title=title,
                jsonData=json_data,
                category_id=category_id,
                user=request.user,
                is_approved=True,
                is_flagged=False
            )
            
            return Response({
                'message': 'JSON이 성공적으로 등록되었습니다',
                'json': json_obj.to_dict()
            }, status=201)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['get'])
    def my_jsons(self, request):
        """내가 등록한 JSON 조회"""
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다'}, status=401)
            
        my_jsons = Jsons.objects.filter(user=request.user)
        serializer = self.get_serializer(my_jsons, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def as_json(self, request, pk=None):
        json_obj = self.get_object()
        try:
            return Response({
                'id': json_obj.id,
                'title': json_obj.title,
                'category': json_obj.category.name if json_obj.category else None,
                'json_data': json_obj.jsonData,
                'user': json_obj.user.username if json_obj.user else None,
                'created_at': json_obj.created_at
            })
        except Exception as e:
            return Response({'error': f'JSON 처리 오류: {str(e)}'}, status=400)
    
    @action(detail=False, methods=['post'])
    def validate_json(self, request):
        """JSON 유효성 검사"""
        json_data = request.data.get('jsonData')
        if not json_data:
            return Response({'error': 'JSON 데이터가 필요합니다'}, status=400)
        
        try:
            # JSON 형식 검사
            if isinstance(json_data, str):
                json.loads(json_data)
            
            # 검열 검사
            profanity_result = check_json_profanity(json_data)
            
            return Response({
                'valid': True,
                'is_clean': profanity_result['is_clean'],
                'message': '유효한 JSON입니다.' if profanity_result['is_clean'] else '욕설이나 금지어가 포함되어 있습니다.'
            })
        except json.JSONDecodeError:
            return Response({'valid': False, 'error': '잘못된 JSON 형식입니다'}, status=400)
        except Exception as e:
            return Response({'valid': False, 'error': str(e)}, status=400)

class JsonBannedWordsViewSet(viewsets.ModelViewSet):
    queryset = JsonBannedWords.objects.all()
    serializer_class = JsonBannedWordsSerializer
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': '관리자 권한이 필요합니다'}, status=403)
            
        word = request.data.get('word', '').strip()
        reason = request.data.get('reason', '')
        
        if not word:
            return Response({'error': '금지어가 필요합니다'}, status=400)
        
        if JsonBannedWords.objects.filter(word=word).exists():
            return Response({'error': '이미 존재하는 금지어입니다'}, status=400)
        
        banned_word = JsonBannedWords.objects.create(
            word=word,
            reason=reason,
            added_by=request.user
        )
        
        return Response({
            'message': '금지어가 추가되었습니다',
            'word': word,
            'reason': reason
        }, status=201)