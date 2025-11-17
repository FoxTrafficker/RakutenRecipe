# recipes/views.py
import json

import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services import get_recipes_by_category

APP_ID = "1044782825325736656"
MAP_PATH = "./script/genre_category_mapping/simple_full_word_mapping.json"

from django.shortcuts import render

def index(request):
    return render(request, "index.html")

class Recipe:
    def __init__(self):
        with open(MAP_PATH, 'r', encoding='utf') as f:
            self.map = json.load(f)

    def get_recipe_by_genre(self, genre_id):
        return self.map.get(genre_id, None)


@require_GET
def recipe(request):
    recipe = Recipe()
    food_genreId = request.GET.get("food_genreId")
    if not food_genreId:
        return JsonResponse({
            "code": 400,
            "msg": "can not find food_genreId",
            "data": []
        }, status=400)
    category_id = recipe.get_recipe_by_genre(food_genreId)

    limit_str = request.GET.get("limit", "5")
    try:
        limit = int(limit_str)
    except ValueError:
        return JsonResponse({
            "code": 400,
            "msg": "limit must be integer value",
            "data": []
        }, status=400)

    try:
        recipes = get_recipes_by_category(category_id, limit=limit)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "code": 502,
            "msg": f"fail when calling Rakuten API: {e}",
            "data": []
        }, status=502)
    except Exception as e:
        return JsonResponse({
            "code": 500,
            "msg": f"server error: {e}",
            "data": []
        }, status=500)

    return JsonResponse({
        "code": 0,
        "msg": "success",
        "data": recipes
    }, json_dumps_params={"ensure_ascii": False}, )
