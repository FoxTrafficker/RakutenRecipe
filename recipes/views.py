# recipes/views.py
import json

import requests
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.http import require_GET

from .services import get_recipes_by_category, get_ranking_by_genre, search_ichiba_items

APP_ID = "1044782825325736656"
MAP_PATH = "./script/genre_category_mapping/simple_full_word_mapping.json"


def index(request):
    return render(request, "index.html")


def food(request):
    return render(request, "food.html")


class Recipe:
    def __init__(self):
        with open(MAP_PATH, 'r', encoding='utf') as f:
            self.map = json.load(f)

    def get_recipe_by_genre(self, genre_id):
        return self.map.get(genre_id, None)


@require_GET
def get_recipe(request):
    recipe = Recipe()
    food_genreId = request.GET.get("food_genreId")
    if not food_genreId:
        return JsonResponse(
            {"code": 400, "msg": "can not find food_genreId", "data": []}, status=400
        )
    category_id = recipe.get_recipe_by_genre(food_genreId)

    limit_str = request.GET.get("limit", "5")
    try:
        limit = int(limit_str)
    except ValueError:
        return JsonResponse(
            {"code": 400, "msg": "limit must be integer value", "data": []}, status=400
        )

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

    # Response
    return JsonResponse({
        "code": 0,
        "msg": "success",
        "data": recipes
    }, json_dumps_params={"ensure_ascii": False, 'indent': 4}, )


@require_GET
def ichiba_ranking(request):
    """
    GET /ichiba_ranking?genreId=100227&page=1
    """
    # genreId
    genre_id = request.GET.get("genreId")
    if not genre_id:
        return JsonResponse({
            "code": 400,
            "msg": "can not find genreId",
            "data": []
        }, status=400)

    # page
    page_str = request.GET.get("page", "1")
    try:
        page = int(page_str)
    except ValueError:
        return JsonResponse({
            "code": 400,
            "msg": "page must be integer value",
            "data": []
        }, status=400)

    # Rakuten API
    try:
        items = get_ranking_by_genre(genre_id, page=page)
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

    # Response
    return JsonResponse({
        "code": 0,
        "msg": "success",
        "data": items
    }, json_dumps_params={"ensure_ascii": False, 'indent': 4}, )


@require_GET
def ichiba_item_search(request):
    """
    GET /ichiba_item_search?keyword=オレンジ&page=1&hits=10

    Keyword-only Rakuten Ichiba Item Search wrapper.
    """

    keyword = request.GET.get("keyword")
    if not keyword:
        return JsonResponse({
            "code": 400,
            "msg": "'keyword' is required.",
            "data": {}
        }, status=400)

    page_str = request.GET.get("page", "1")
    hits_str = request.GET.get("hits", "30")
    sort = request.GET.get("sort")  # optional

    try:
        page = int(page_str)
        hits = int(hits_str)
    except ValueError:
        return JsonResponse({
            "code": 400,
            "msg": "'page' and 'hits' must be integers.",
            "data": {}
        }, status=400)

    if hits < 1 or hits > 30:
        return JsonResponse({
            "code": 400,
            "msg": "'hits' must be between 1 and 30.",
            "data": {}
        }, status=400)

    try:
        api_result = search_ichiba_items(
            keyword=keyword,
            page=page,
            hits=hits,
            sort=sort,
        )
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "code": 502,
            "msg": f"Rakuten Ichiba Item Search API request failed: {e}",
            "data": {}
        }, status=502)
    except Exception as e:
        return JsonResponse({
            "code": 500,
            "msg": f"Internal server error: {e}",
            "data": {}
        }, status=500)

    return JsonResponse({
        "code": 0,
        "msg": "success",
        "data": api_result,
    }, json_dumps_params={"ensure_ascii": False, 'indent': 4})


def recipe(request):
    return render(request, "recipe.html")
