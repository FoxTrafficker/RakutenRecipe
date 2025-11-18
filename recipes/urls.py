# recipes/urls.py
from django.urls import path
from .views import recipe, ichiba_ranking, ichiba_item_search, get_recipe
from .views import index, food

urlpatterns = [
    path("", index, name="index"),
    path("food", food, name="food"),
    path("recipe/", recipe, name="recipe"),
    path("api/get_recipe/", get_recipe, name="get_recipe"),
    path("ichiba_ranking", ichiba_ranking, name="ichiba_ranking"),
    path("ichiba_item_search", ichiba_item_search, name="ichiba_item_search"),
]
