# recipes/urls.py
from django.urls import path
from .views import recipe, get_recipe
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("recipe/", recipe, name="recipe"),
    path("api/get_recipe/", get_recipe, name="get_recipe"),
]
