from django.urls import path

from .views import category_list, recipe_detail, recipe_list

app_name = "recipes"

urlpatterns = [
    path("", recipe_list, name="recipe-list"),
    path("recipes/<slug:slug>/", recipe_detail, name="recipe-detail"),
    path("categories/", category_list, name="category-list"),
]
