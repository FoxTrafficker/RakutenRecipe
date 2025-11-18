import requests

APP_ID = "1044782825325736656"


def get_recipes_by_category(category_id, limit=5):
    url = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2,
        "categoryId": category_id,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    recipes = []
    for r in data.get("result", [])[:limit]:
        recipes.append({
            "recipeId": r["recipeId"],
            "title": r["recipeTitle"],
            "url": r["recipeUrl"],
            "image": r.get("mediumImageUrl") or r.get("foodImageUrl"),
            "materials": r.get("recipeMaterial", []),
            "time": r.get("recipeIndication"),
            "cost": r.get("recipeCost"),
            "rank": int(r["rank"]),
            "author": r.get("nickname"),
        })
    return recipes


def get_ranking_by_genre(genre_id, page=1):
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2,
        "genreId": genre_id,
        "page": page,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("Items", [])
    return items


def search_ichiba_items(keyword, page=1, hits=30, sort=None):
    """
    Rakuten Ichiba Item Search API
    Documentation: https://webservice.rakuten.co.jp/documentation/ichiba-item-search

    keyword must be provided.
    """
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2,
        "page": page,
        "hits": hits,  # 1–30
        "keyword": keyword,
    }

    if sort:
        # e.g. +itemPrice / -itemPrice / -reviewAverage
        params["sort"] = sort

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_item_detail_by_code(item_code: str):
    """
    Use Ichiba Item Search API with itemCode to get single item detail.
    """
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2,
        "itemCode": item_code,
        "hits": 1,  # 只要一条
        "page": 1,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("Items") or data.get("items") or []
    if not items:
        return None

    # formatVersion=2 时就是列表里直接是 item 对象
    item = items[0]
    return item
