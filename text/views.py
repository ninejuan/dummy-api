from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Texts, TextCategories, TCPeering
from django.views.decorators.http import require_http_methods
import json

### Required Features
# Create : add category, add new value, add new link 
# Get : list all categories, list all values by category, get value(s) by (random, id), get value(s) by category, get all values, get all links
# Update : update category, update value
# Delete : delete category, delete value, delete link
#
# response type : json
###

@require_http_methods(["GET"])
def get_all_categories(request):
    categories = TextCategories.objects.all().values()
    return JsonResponse(list(categories), safe=False)

@require_http_methods(["GET"])
def get_all_values(request):
    values = Texts.objects.all().values()
    return JsonResponse(list(values), safe=False)

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

@require_http_methods(["POST"])
def add_category(request):
    data = json.loads(request.body)
    category = TextCategories.objects.create(name=data['name'])
    return JsonResponse(category.to_dict(), status=201)

@require_http_methods(["POST"])
def add_value(request):
    data = json.loads(request.body)
    category = get_object_or_404(TextCategories, id=data['category_id'])
    value = Texts.objects.create(text=data['text'], category=category)
    return JsonResponse(value.to_dict(), status=201)

@require_http_methods(["POST"])
def add_link(request):
    data = json.loads(request.body)
    link = TCPeering.objects.create(source=data['source'], target=data['target'])
    return JsonResponse(link.to_dict(), status=201)

@require_http_methods(["PUT"])
def update_category(request, category_id):
    data = json.loads(request.body)
    category = get_object_or_404(TextCategories, id=category_id)
    category.name = data['name']
    category.save()
    return JsonResponse(category.to_dict())

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

@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    category = get_object_or_404(TextCategories, id=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully'})

@require_http_methods(["DELETE"])
def delete_value(request, value_id):
    value = get_object_or_404(Texts, id=value_id)
    value.delete()
    return JsonResponse({'message': 'Value deleted successfully'})

@require_http_methods(["DELETE"])
def delete_link(request, link_id):
    link = get_object_or_404(TCPeering, id=link_id)
    link.delete()
    return JsonResponse({'message': 'Link deleted successfully'})

