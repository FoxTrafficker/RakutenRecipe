import json

import requests

APP_ID = "1044782825325736656"
MAP_PATH = "./genre_category_mapping/simple_full_word_mapping.json"


class Recipe:
    def __init__(self):
        with open(MAP_PATH, 'r', encoding='utf') as f:
            self.map = json.load(f)

    def get_recipe_by_genre(self, genre_id):
        return self.map.get(genre_id, None)


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


if __name__ == "__main__":
    recipe = Recipe()

    FOOD_GENRE = 100227  # 食品
    ranking = get_ranking_by_genre(FOOD_GENRE)

    print("=== 食品ランキング===")
    for item in ranking:
        print(item)
        print(recipe.get_recipe_by_genre(genre_id=item['genreId']))
