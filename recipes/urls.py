# recipes/urls.py
from django.urls import path
from .views import recipe, ichiba_ranking
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("recipe", recipe, name="recipe"),
    path("ichiba_ranking", ichiba_ranking, name="ichiba_ranking"),
]
