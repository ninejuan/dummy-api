from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Texts, TextCategories
from django.views.decorators.http import require_http_methods
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
def get_texts_by_category(request, category_id):
    values = Texts.objects.filter(category_id=category_id)
    if not values.exists():
        return JsonResponse({'error': '해당 카테고리의 텍스트가 없습니다'}, status=404)
    return JsonResponse([value.to_dict() for value in values], safe=False)

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
