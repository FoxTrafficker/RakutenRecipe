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
