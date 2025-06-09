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
# @csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 텍스트 카테고리 조회",
    responses={
        200: openapi.Response(description="카테고리 조회 성공", schema=openapi.Schema(
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
        )),
        404: openapi.Response(description="카테고리가 없음")
    },
)
@require_http_methods(["GET"])
def get_all_categories(request):
    categories = TextCategories.objects.all()
    if not categories.exists():
        return JsonResponse({'error': '카테고리가 없습니다'}, status=404)
    return JsonResponse([category.to_dict() for category in categories], safe=False)

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
def get_all_values(request):
    try:
        values = Texts.objects.all()
        if not values.exists():
            return JsonResponse({'error': '텍스트가 없습니다'}, status=404)
        return JsonResponse([value.to_dict() for value in values], safe=False)
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
def get_values_by_category(request, category_id):
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
def get_value_by_id(request, value_id):
    value = get_object_or_404(Texts, id=value_id)
    return JsonResponse(value.to_dict())

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
def get_random_value(request):
    import random
    values = list(Texts.objects.all())
    if not values:
        return JsonResponse({'error': '텍스트가 없습니다'}, status=404)
    value = random.choice(values)
    return JsonResponse(value.to_dict())
