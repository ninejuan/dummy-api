from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Texts, TextCategories, TCPeering
from django.views.decorators.http import require_http_methods
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

### Required Features
# Create : add category, add new value, add new link 
# Get : list all categories, list all values by category, get value(s) by (random, id), get value(s) by category, get all values, get all links
# Update : update category, update value
# Delete : delete category, delete value, delete link
#
# response type : json
###

"""
GET METHODS
"""
@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get all categories",
    responses={
    200: openapi.Response(description="Successfully retrieved all categories", schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the category'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Creation timestamp'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Last update timestamp')
            }
        )
    )),
    404: openapi.Response(description="No categories found")
    },
)
@require_http_methods(["GET"])
def get_all_categories(request):
    print('hi')
    categories = TextCategories.objects.all().values()
    return JsonResponse(list(categories), safe=False)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 텍스트 값 조회",
    responses={
        200: openapi.Response(description="텍스트 값 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='텍스트 ID'),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description='텍스트 내용'),
                    'category': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리', nullable=True),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                }
            )
        )),
        404: openapi.Response(description="텍스트 값이 없음")
    },
)
@require_http_methods(["GET"])
def get_all_values(request):
    try:
        values = Texts.objects.all()
        if not values.exists():
            return JsonResponse({'error': '텍스트 값이 없습니다'}, status=404)
            
        values_list = []
        for value in values:
            value_dict = value.to_dict()
            # 카테고리 정보 가져오기
            if value.category:
                value_dict['category_name'] = value.category.category_name
            values_list.append(value_dict)
            
        return JsonResponse(values_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_all_links(request):
    links = TCPeering.objects.all().values()
    return JsonResponse(list(links), safe=False)

@require_http_methods(["GET"])
def get_values_by_category(request, category_id):
    values = Texts.objects.filter(category_id=category_id).values()
    return JsonResponse(list(values), safe=False)

@require_http_methods(["GET"])
def get_value_by_id(request, value_id):
    value = get_object_or_404(Texts, id=value_id)
    return JsonResponse(value.to_dict())

@require_http_methods(["GET"])
def get_random_value(request):
    import random
    values = list(Texts.objects.all())
    if not values:
        return JsonResponse({'error': 'No values available'}, status=404)
    value = random.choice(values)
    return JsonResponse(value.to_dict())

"""
POST METHODS
"""
@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(
    operation_description="Add a new category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the category'),
        },
    ),
    responses={
        201: openapi.Response(description="Category created successfully"),
        400: openapi.Response(description="Bad request - Invalid data"),
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
@require_http_methods(["POST"])
def add_category(request):
    data = json.loads(request.body)
    category = TextCategories.objects.create(name=data['name'])
    return JsonResponse(category.to_dict(), status=201)

@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(
    operation_description="Add a new text value",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='Text content'),
        },
    ),
    responses={
        201: openapi.Response(description="Value created successfully"),
        400: openapi.Response(description="Bad request - Invalid data"),
        404: openapi.Response(description="Category not found"),
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
@require_http_methods(["POST"])
def add_value(request):
    data = json.loads(request.body)
    category = get_object_or_404(TextCategories, id=data['category_id'])
    value = Texts.objects.create(text=data['text'], category=category)
    return JsonResponse(value.to_dict(), status=201)

@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(
    operation_description="Add a new link between two texts",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'text_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Source text ID'),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Target text ID'),
        },
    ),
    responses={
        201: openapi.Response(description="Link created successfully"),
        400: openapi.Response(description="Bad request - Invalid data"),
        404: openapi.Response(description="Source or target text not found"),
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
@require_http_methods(["POST"])
def add_link(request):
    data = json.loads(request.body)
    link = TCPeering.objects.create(
        text=get_object_or_404(Texts, id=data['text_id']),
        category=get_object_or_404(TextCategories, id=data['category_id'])
    )
    return JsonResponse(link.to_dict(), status=201)

"""
PUT METHODS
"""
@csrf_exempt
@api_view(['PUT'])
@swagger_auto_schema(
    operation_description="Update a category by ID",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the category'),
        },
    ),
    responses={
        200: openapi.Response(description="Category updated successfully"),
        404: openapi.Response(description="Category not found"),
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
@require_http_methods(["PUT"])
def update_category(request, category_id):
    data = json.loads(request.body)
    category = get_object_or_404(TextCategories, id=category_id)
    category.name = data['name']
    category.save()
    return JsonResponse(category.to_dict())

@csrf_exempt
@api_view(['PUT'])
@swagger_auto_schema(
    operation_description="Update a text value by ID",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='Text content'),
        },
    ),
    responses={
        200: openapi.Response(description="Value updated successfully"),
        404: openapi.Response(description="Value or Category not found"),
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
@require_http_methods(["PUT"])
def update_value(request, value_id):
    data = json.loads(request.body)
    value = get_object_or_404(Texts, id=value_id)
    value.text = data['text']
    if 'category_id' in data:
        category = get_object_or_404(TextCategories, id=data['category_id'])
        value.category = category
    value.save()
    return JsonResponse(value.to_dict())

"""
DELETE METHODS
Needs admin authentication
"""

@csrf_exempt
@api_view(['DELETE'])
@swagger_auto_schema(
    operation_description="Delete a category by ID",
    responses={
        204: openapi.Response(description="Category deleted successfully"),
        403: openapi.Response(description="Permission denied - Admin access required")
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_category(request, category_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied - Admin access required'}, status=403)
    category = get_object_or_404(TextCategories, id=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully'}, status=204)

@csrf_exempt
@api_view(['DELETE'])
@swagger_auto_schema(
    operation_description="Delete a value by ID",
    responses={
        204: openapi.Response(description="Value deleted successfully"),
        403: openapi.Response(description="Permission denied - Admin access required")
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_value(request, value_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied - Admin access required'}, status=403)
    value = get_object_or_404(Texts, id=value_id)
    value.delete()
    return JsonResponse({'message': 'Value deleted successfully'}, status=204)

@csrf_exempt
@api_view(['DELETE'])
@swagger_auto_schema(
    operation_description="Delete a link by ID",
    responses={
        204: openapi.Response(description="Link deleted successfully"),
        403: openapi.Response(description="Permission denied - Admin access required")
    },
)
@permission_classes([IsAuthenticated, IsAdminUser])
async def delete_link(request, link_id):
    print(request.user)
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied - Admin access required'}, status=403)
    link = await get_object_or_404(TCPeering, id=link_id)
    link.delete()
    return JsonResponse({'message': 'Link deleted successfully'}, status=204)
