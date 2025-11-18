import json
from unittest.mock import patch, Mock

from recipes.services import get_recipes_by_category

SAMPLE_API_RESPONSE = {
    "result": [
        {
            "recipeId": "12345",
            "recipeTitle": "テストレシピ",
            "recipeUrl": "https://example.com/recipe/12345",
            "mediumImageUrl": "https://example.com/img/12345.jpg",
            "recipeMaterial": ["材料1", "材料2"],
            "recipeIndication": "10分",
            "recipeCost": "300円",
            "rank": "1",
            "nickname": "cook"
        },
        {
            "recipeId": "67890",
            "recipeTitle": "別レシピ",
            "recipeUrl": "https://example.com/recipe/67890",
            "foodImageUrl": "https://example.com/img/67890.jpg",
            "recipeMaterial": [],
            "recipeIndication": "20分",
            "recipeCost": "500円",
            "rank": "2",
            "nickname": "chef"
        }
    ]
}


def make_mock_resp(data):
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json = Mock(return_value=data)
    return mock_resp


@patch("recipes.services.requests.get")
def test_get_recipes_by_category_success(mock_get):
    mock_get.return_value = make_mock_resp(SAMPLE_API_RESPONSE)

    res = get_recipes_by_category("10", limit=2)
    assert isinstance(res, list)
    assert len(res) == 2

    first = res[0]
    assert first["recipeId"] == "12345"
    assert first["title"] == "テストレシピ"
    assert first["url"] == "https://example.com/recipe/12345"
    assert first["image"] == "https://example.com/img/12345.jpg"
    assert first["materials"] == ["材料1", "材料2"]
    assert first["time"] == "10分"
    assert first["cost"] == "300円"
    assert first["rank"] == 1
    assert first["author"] == "cook"


@patch("recipes.services.requests.get")
def test_get_recipes_by_category_limit(mock_get):
    mock_get.return_value = make_mock_resp(SAMPLE_API_RESPONSE)

    res = get_recipes_by_category("10", limit=1)
    assert len(res) == 1