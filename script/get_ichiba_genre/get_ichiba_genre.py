import json
import time
import requests

APP_ID = "1044782825325736656"


def get_child_genre(genre_id=0):
    """
    用 Rakuten IchibaGenre/Search API 获取某个 genreId 的直接子分类（children）
    返回: [{genreId, genreLevel, genreName}, ...]
    """
    url = "https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20120723"
    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2,
        "genreId": genre_id,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    children = []
    for ch in data.get("children", []):
        # 对于 formatVersion=2，children 里的每个元素就是子分类本身
        child = ch
        children.append({
            "genreId": child["genreId"],
            "genreLevel": child["genreLevel"],
            "genreName": child["genreName"],
        })
    return children


def build_genre_tree(root_genre_id, root_genre_name=None, root_genre_level=1,
                     visited=None, sleep_sec=0.2):
    """
    递归构建某个根 genreId 下的完整分类树。

    返回结构:
    {
        "genreId": ...,
        "genreName": ...,
        "genreLevel": ...,
        "children": [ {...}, {...}, ... ]
    }
    """
    if visited is None:
        visited = set()

    # 防止意外循环
    if root_genre_id in visited:
        return None
    visited.add(root_genre_id)

    # 当前节点
    node = {
        "genreId": root_genre_id,
        "genreName": root_genre_name,
        "genreLevel": root_genre_level,
        "children": []
    }

    # 获取当前 genre 的直接子类
    children = get_child_genre(root_genre_id)

    # 递归构建每个子类的子树
    for ch in children:
        child_id = ch["genreId"]
        child_name = ch["genreName"]
        child_level = ch["genreLevel"]

        print(ch)

        # 稍微 sleep 一下，避免短时间内请求过快（简单防止被限流）
        time.sleep(sleep_sec)

        child_node = build_genre_tree(
            root_genre_id=child_id,
            root_genre_name=child_name,
            root_genre_level=child_level,
            visited=visited,
            sleep_sec=sleep_sec
        )
        if child_node is not None:
            node["children"].append(child_node)

    return node


if __name__ == "__main__":
    # 食品大类
    FOOD_GENRE_ID = 100227
    FOOD_GENRE_NAME = "食品"  # 如果想更严谨也可以先调一次 API 拿名字，这里直接写死也OK
    FOOD_GENRE_LEVEL = 1

    print("正在构建『食品』分类树，请稍等……")

    food_tree = build_genre_tree(
        root_genre_id=FOOD_GENRE_ID,
        root_genre_name=FOOD_GENRE_NAME,
        root_genre_level=FOOD_GENRE_LEVEL,
        sleep_sec=5  # 可以根据需要调整请求间隔
    )

    # 打印部分结果看一下
    print("构建完成，部分输出预览：")
    print(json.dumps(food_tree, ensure_ascii=False, indent=2)[:1000], "...\n")

    # 保存为 JSON 文件
    output_file = "food_genres.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(food_tree, f, ensure_ascii=False, indent=2)

    print(f"已保存到 {output_file}")
