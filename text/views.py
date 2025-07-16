from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Texts, TextCategories, BannedWords
from django.views.decorators.http import require_http_methods
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import korcen

"""
GET METHODS
"""
@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 텍스트 카테고리 조회 (페이지네이션)",
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
        
        categories = TextCategories.objects.all()
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
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 텍스트 조회",
    responses={
        200: openapi.Response(description="텍스트 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='텍스트 ID'),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description='텍스트 내용'),
                    'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                }
            )
        )),
        404: openapi.Response(description="텍스트가 없음")
    },
)
@require_http_methods(["GET"])
def get_all_texts(request, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        values = Texts.objects.all()
        if not values.exists():
            return JsonResponse({'error': '텍스트가 없습니다'}, status=404)
            
        total_count = values.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_values = values[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'texts': [value.to_dict() for value in paginated_values]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="카테고리별 텍스트 조회",
    responses={
        200: openapi.Response(description="텍스트 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 텍스트 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'texts': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='텍스트 ID'),
                            'text': openapi.Schema(type=openapi.TYPE_STRING, description='텍스트 내용'),
                            'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="텍스트가 없음")
    },
)
@require_http_methods(["GET"])
def get_texts_by_category(request, category_id, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        values = Texts.objects.filter(category_id=category_id)
        if not values.exists():
            return JsonResponse({'error': '해당 카테고리의 텍스트가 없습니다'}, status=404)
            
        total_count = values.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_values = values[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'texts': [value.to_dict() for value in paginated_values]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="ID로 텍스트 조회",
    responses={
        200: openapi.Response(description="텍스트 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='텍스트 ID'),
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='텍스트 내용'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="텍스트를 찾을 수 없음")
    },
)
@require_http_methods(["GET"])
def get_text_by_id(request, value_id):
    value = get_object_or_404(Texts, id=value_id)
    return JsonResponse(value.to_dict())

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="카테고리 이름으로 카테고리 정보 조회",
    responses={
        200: openapi.Response(description="카테고리 정보 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='카테고리 ID'),
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 이름'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 설명'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="카테고리를 찾을 수 없음")
    },
)
@require_http_methods(["GET"])
def get_category_info(request, category_name):
    try:
        category = get_object_or_404(TextCategories, category_name=category_name)
        return JsonResponse(category.to_dict())
    except TextCategories.DoesNotExist:
        return JsonResponse({'error': '카테고리를 찾을 수 없습니다'}, status=404)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="랜덤 텍스트 조회",
    responses={
        200: openapi.Response(description="텍스트 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='텍스트 ID'),
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='텍스트 내용'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="텍스트가 없음")
    },
)
@require_http_methods(["GET"])
def get_random_text(request):
    import random
    values = list(Texts.objects.all())
    if not values:
        return JsonResponse({'error': '텍스트가 없습니다'}, status=404)
    value = random.choice(values)
    return JsonResponse(value.to_dict())

def check_profanity(text):
    """욕설 및 금지어 검사"""
    # korcen으로 욕설 검사
    profanity_checker = korcen.ProfanityChecker()
    is_profane = profanity_checker.check(text)
    
    # 금지어 검사
    banned_words = BannedWords.objects.all()
    found_banned_words = []
    
    for banned_word in banned_words:
        if banned_word.word.lower() in text.lower():
            found_banned_words.append(banned_word.word)
    
    return {
        'is_profane': is_profane,
        'found_banned_words': found_banned_words,
        'is_clean': not is_profane and len(found_banned_words) == 0
    }

"""
POST METHODS - 사용자 참여형 기능
"""
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="사용자가 텍스트 등록 (로그인 필요)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['text'],
        properties={
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='등록할 텍스트'),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='카테고리 ID (선택사항)')
        }
    ),
    responses={
        201: openapi.Response(description="텍스트 등록 성공"),
        400: openapi.Response(description="잘못된 요청"),
        403: openapi.Response(description="검열 실패 - 욕설/금지어 포함")
    }
)
def create_user_text(request):
    try:
        data = json.loads(request.body)
        text_content = data.get('text', '').strip()
        category_id = data.get('category_id')
        
        if not text_content:
            return JsonResponse({'error': '텍스트 내용이 필요합니다'}, status=400)
        
        # 검열 검사
        profanity_result = check_profanity(text_content)
        
        if not profanity_result['is_clean']:
            # 검열 실패 시에도 저장하되 승인되지 않은 상태로
            text_obj = Texts.objects.create(
                text=text_content,
                user=request.user,
                category_id=category_id,
                is_approved=False,
                is_flagged=True,
                flagged_reason=f"욕설 포함: {profanity_result['is_profane']}, 금지어: {', '.join(profanity_result['found_banned_words'])}"
            )
            
            return JsonResponse({
                'error': '욕설이나 금지어가 포함되어 승인되지 않았습니다',
                'flagged_reason': text_obj.flagged_reason,
                'text_id': text_obj.id
            }, status=403)
        
        # 검열 통과 시 정상 저장
        text_obj = Texts.objects.create(
            text=text_content,
            user=request.user,
            category_id=category_id,
            is_approved=True,
            is_flagged=False
        )
        
        return JsonResponse({
            'message': '텍스트가 성공적으로 등록되었습니다',
            'text': text_obj.to_dict()
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="내가 등록한 텍스트 조회",
    responses={
        200: openapi.Response(description="내 텍스트 조회 성공"),
        404: openapi.Response(description="등록한 텍스트가 없음")
    }
)
def get_my_texts(request, page=1, limit=10):
    try:
        page = int(page)
        limit = int(limit)
        
        my_texts = Texts.objects.filter(user=request.user)
        if not my_texts.exists():
            return JsonResponse({'error': '등록한 텍스트가 없습니다'}, status=404)
        
        total_count = my_texts.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_texts = my_texts[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'texts': [text.to_dict() for text in paginated_texts]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="승인된 텍스트만 조회",
    responses={
        200: openapi.Response(description="승인된 텍스트 조회 성공"),
        404: openapi.Response(description="승인된 텍스트가 없음")
    }
)
def get_approved_texts(request, page=1, limit=10):
    try:
        page = int(page)
        limit = int(limit)
        
        approved_texts = Texts.objects.filter(is_approved=True)
        if not approved_texts.exists():
            return JsonResponse({'error': '승인된 텍스트가 없습니다'}, status=404)
        
        total_count = approved_texts.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_texts = approved_texts[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'texts': [text.to_dict() for text in paginated_texts]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

"""
금지어 관리 (관리자 전용)
"""
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
@swagger_auto_schema(
    operation_description="금지어 추가 (관리자 전용)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['word'],
        properties={
            'word': openapi.Schema(type=openapi.TYPE_STRING, description='금지할 단어'),
            'reason': openapi.Schema(type=openapi.TYPE_STRING, description='금지 사유')
        }
    ),
    responses={
        201: openapi.Response(description="금지어 추가 성공"),
        400: openapi.Response(description="이미 존재하는 금지어")
    }
)
def add_banned_word(request):
    try:
        data = json.loads(request.body)
        word = data.get('word', '').strip()
        reason = data.get('reason', '')
        
        if not word:
            return JsonResponse({'error': '금지어가 필요합니다'}, status=400)
        
        # 이미 존재하는지 확인
        if BannedWords.objects.filter(word=word).exists():
            return JsonResponse({'error': '이미 존재하는 금지어입니다'}, status=400)
        
        banned_word = BannedWords.objects.create(
            word=word,
            reason=reason,
            added_by=request.user
        )
        
        return JsonResponse({
            'message': '금지어가 추가되었습니다',
            'word': word,
            'reason': reason
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="금지어 목록 조회",
    responses={
        200: openapi.Response(description="금지어 목록 조회 성공")
    }
)
def get_banned_words(request):
    banned_words = BannedWords.objects.all()
    words_list = [{'id': word.id, 'word': word.word, 'reason': word.reason} for word in banned_words]
    return JsonResponse({'banned_words': words_list})

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@swagger_auto_schema(
    operation_description="금지어 삭제 (관리자 전용)",
    responses={
        200: openapi.Response(description="금지어 삭제 성공"),
        404: openapi.Response(description="금지어를 찾을 수 없음")
    }
)
def delete_banned_word(request, word_id):
    try:
        banned_word = get_object_or_404(BannedWords, id=word_id)
        word_text = banned_word.word
        banned_word.delete()
        
        return JsonResponse({
            'message': f'금지어 "{word_text}"가 삭제되었습니다'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(
    operation_description="텍스트 검열 테스트",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['text'],
        properties={
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='검열할 텍스트')
        }
    ),
    responses={
        200: openapi.Response(description="검열 결과")
    }
)
def test_censorship(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        
        profanity_result = check_profanity(text)
        
        return JsonResponse({
            'text': text,
            'is_clean': profanity_result['is_clean'],
            'is_profane': profanity_result['is_profane'],
            'found_banned_words': profanity_result['found_banned_words'],
            'can_be_posted': profanity_result['is_clean']
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
