import json
import requests

APP_ID = "1044782825325736656"


def get_categories():
    """
    获取楽天レシピ分类列表（CategoryList API）
    返回 formatVersion=2 的 JSON 字典
    """
    url = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426"
    params = {
        "applicationId": APP_ID,
        "format": "json",
        "formatVersion": 2
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    print("正在获取楽天レシピ分类，请稍等...")

    data = get_categories()

    # 预览打印前 500 字符
    print("获取成功，部分预览：")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:500], "...\n")

    # 保存为 JSON 文件
    output = "recipe_categories.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已保存到文件：{output}")
