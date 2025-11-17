import json

# 文件路径（你可修改）
FOOD_JSON = "../get_ichiba_genre/food_genres.json"
RECIPE_JSON = "../get_recipe_categories/recipe_categories.json"


def load_food_genres():
    def _flatten_genre_tree(node, parent_id=None, parent_path=""):
        flat = []

        genre_id = node.get("genreId")
        genre_name = node.get("genreName")
        genre_level = node.get("genreLevel")

        # 当前节点的路径
        if parent_path:
            path = f"{parent_path} > {genre_name}"
        else:
            path = genre_name or ""

        flat.append({
            "genreId": genre_id,
            "genreName": genre_name,
            "genreLevel": genre_level,
            "parentId": parent_id,
            "path": path,
        })

        # 递归子节点
        for child in node.get("children", []):
            flat.extend(_flatten_genre_tree(child, parent_id=genre_id, parent_path=path))

        return flat

    with open(FOOD_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    flat = []

    # 兼容两种情况：根是 dict 或 list
    if isinstance(data, dict):
        flat = _flatten_genre_tree(data)
    elif isinstance(data, list):
        for node in data:
            flat.extend(_flatten_genre_tree(node))
    else:
        raise ValueError("food_genres.json 格式不符合预期（既不是对象也不是数组）")

    return flat


def load_recipe_categories():
    """加载 recipe 分类（large / medium / small）并扁平化"""
    with open(RECIPE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    recipe_list = []
    result = data.get("result", {})

    for level in ["large", "medium", "small"]:
        for cat in result.get(level, []):
            recipe_list.append({
                "categoryId": cat["categoryId"],
                "categoryName": cat["categoryName"],
                "level": level
            })

    return recipe_list


def basic_full_word_mapping(food_categories, recipe_categories):
    """
    基础“全词匹配”：
    genreName 中出现某个 recipe_categoryName 的部分片段
    """
    full_map = {}
    simple_map = {}
    for food in food_categories:
        f_id = food["genreId"]
        f_name = food["genreName"]

        matched = []

        for rec in recipe_categories:
            r_id = rec["categoryId"]
            r_name = rec["categoryName"]

            if (r_name in f_name) or (f_name in r_name):
                print(f"{r_name}, {r_id} -> {f_name}, {f_id}")

                simple_map[f_id] = r_id
                matched.append({
                    "recipeId": r_id,
                    "recipeName": r_name,
                    "recipeLevel": rec["level"]
                })

        full_map[f_id] = {
            "genreName": f_name,
            "matched": matched
        }

    return full_map, simple_map


if __name__ == "__main__":
    food = load_food_genres()
    recipe = load_recipe_categories()
    full_map, simple_map = basic_full_word_mapping(food, recipe)

    with open("full_word_mapping.json", "w", encoding="utf-8") as f:
        json.dump(full_map, f, ensure_ascii=False, indent=2)
    with open("simple_full_word_mapping.json", "w", encoding="utf-8") as f:
        json.dump(simple_map, f, ensure_ascii=False, indent=2)
