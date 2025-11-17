import requests

APP_ID = "1044782825325736656"


def get_recipes_by_category(category_id, limit=5):
    """
    根据 Recipe 的 categoryId 获取该分类下的热门菜单列表
    返回: 一个菜谱列表，每个包含标题/图片/链接/材料等
    """
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
            "time": r.get("recipeIndication"),  # 时间：5分 / 約30分 等
            "cost": r.get("recipeCost"),  # 费用：300円前後 等
            "rank": int(r["rank"]),
            "author": r.get("nickname"),
        })
    return recipes


if __name__ == "__main__":
    cat_id = "10-276"  # 举例：豚肉
    recipes = get_recipes_by_category(cat_id, limit=10)

    for r in recipes:
        print(r)
