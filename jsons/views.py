from django.shortcuts import render
from django.http import JsonResponse
from .models import Jsons, JsonCategory
from django.views.decorators.http import require_http_methods
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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