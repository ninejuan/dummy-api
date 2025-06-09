from django.http import JsonResponse
from .models import Images, ImageCategory
from django.views.decorators.http import require_http_methods
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="모든 이미지 카테고리 조회 (페이지네이션)",
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
                            'description': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 설명'),
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
        
        categories = ImageCategory.objects.all()
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
    operation_description="모든 이미지 조회 (페이지네이션)",
    responses={
        200: openapi.Response(description="이미지 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 이미지 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='이미지 ID'),
                            'imageUrl': openapi.Schema(type=openapi.TYPE_STRING, description='이미지 URL'),
                            'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="이미지가 없음"),
        400: openapi.Response(description="잘못된 페이지 번호 또는 한 페이지당 항목 수")
    },
)
@require_http_methods(["GET"])
def get_all_images(request, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        
        images = Images.objects.all()
        if not images.exists():
            return JsonResponse({'error': '이미지가 없습니다'}, status=404)
            
        total_count = images.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_images = images[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'images': [image.to_dict() for image in paginated_images]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="특정 이미지 카테고리 조회",
    manual_parameters=[openapi.Parameter('category_name', openapi.IN_QUERY, description="카테고리 이름", type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="카테고리 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='카테고리 ID'),
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 이름'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='카테고리 설명'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="카테고리가 없음")
    },
)
@require_http_methods(["GET"])
def get_category_by_name(request, category_name):
    try:
        category = ImageCategory.objects.get(category_name=category_name)
        return JsonResponse(category.to_dict())
    except ImageCategory.DoesNotExist:
        return JsonResponse({'error': '해당 카테고리가 없습니다'}, status=404)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="카테고리 ID로 이미지 조회 (페이지네이션)",
    manual_parameters=[
        openapi.Parameter('category_id', openapi.IN_QUERY, description="카테고리 ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('page', openapi.IN_QUERY, description="페이지 번호", type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, description="한 페이지당 항목 수", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response(description="이미지 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 이미지 수'),
                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description='현재 페이지 번호'),
                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='전체 페이지 수'),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='이미지 ID'),
                            'imageUrl': openapi.Schema(type=openapi.TYPE_STRING, description='이미지 URL'),
                            'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
                        }
                    )
                )
            }
        )),
        404: openapi.Response(description="이미지가 없음"),
        400: openapi.Response(description="잘못된 페이지 번호 또는 한 페이지당 항목 수")
    }
)
@require_http_methods(["GET"])
def get_images_by_category(request, category_id, page=1, limit=10):
    try:
        page = int(page)
        limit = int(limit)
        
        images = Images.objects.filter(category_id=category_id)
        if not images.exists():
            return JsonResponse({'error': '해당 카테고리의 이미지가 없습니다'}, status=404)
            
        total_count = images.count()
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        paginated_images = images[start_index:end_index]
        
        response_data = {
            'total_count': total_count,
            'current_page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'images': [image.to_dict() for image in paginated_images]
        }
        
        return JsonResponse(response_data, safe=False)
    except ValueError:
        return JsonResponse({'error': '페이지 번호와 한 페이지당 항목 수는 숫자여야 합니다'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="특정 이미지 조회",
    manual_parameters=[openapi.Parameter('image_id', openapi.IN_QUERY, description="이미지 ID", type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="이미지 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='이미지 ID'),
                'imageUrl': openapi.Schema(type=openapi.TYPE_STRING, description='이미지 URL'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="이미지를 찾을 수 없음")
    },
)
@require_http_methods(["GET"])
def get_image_by_id(request, image_id):
    try:
        image = Images.objects.get(id=image_id)
        return JsonResponse(image.to_dict())
    except Images.DoesNotExist:
        return JsonResponse({'error': '해당 이미지를 찾을 수 없습니다'}, status=404)

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="랜덤 이미지 조회",
    responses={
        200: openapi.Response(description="이미지 조회 성공", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='이미지 ID'),
                'imageUrl': openapi.Schema(type=openapi.TYPE_STRING, description='이미지 URL'),
                'category': openapi.Schema(type=openapi.TYPE_OBJECT, description='카테고리 정보'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='생성 시간'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='수정 시간')
            }
        )),
        404: openapi.Response(description="이미지가 없음")
    },
)
@require_http_methods(["GET"])
def get_random_image(request):
    import random
    images = Images.objects.all()
    if not images.exists():
        return JsonResponse({'error': '이미지가 없습니다'}, status=404)
    random_image = random.choice(images)
    return JsonResponse(random_image.to_dict())