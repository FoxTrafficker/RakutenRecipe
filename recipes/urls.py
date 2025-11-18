# recipes/urls.py
from django.urls import path

from .views import index, item_detail
from .views import recipe, ichiba_ranking, ichiba_item_search, get_recipe, ichiba_item_detail

urlpatterns = [
    path("", index, name="index"),
    path("item_detail", item_detail, name="item_detail"),
    path("recipe/", recipe, name="recipe"),
    path("api/get_recipe/", get_recipe, name="get_recipe"),
    path("ichiba_ranking", ichiba_ranking, name="ichiba_ranking"),
    path("ichiba_item_search", ichiba_item_search, name="ichiba_item_search"),
    path("ichiba_item_detail", ichiba_item_detail, name="ichiba_item_detail"),
]
