# recipes/urls.py
from django.urls import path
from .views import recipe
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("recipe", recipe, name="recipe"),
]
