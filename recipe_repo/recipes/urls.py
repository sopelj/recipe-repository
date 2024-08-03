from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import category_list, recipe_detail, recipe_list

app_name = "recipes"

urlpatterns = [
    path("", recipe_list, name="recipe-list"),
    path(_("recipes/<slug:slug>/"), recipe_detail, name="recipe-detail"),
    path(_("categories/"), category_list, name="category-list"),
    path(_("categories/<slug:category_slug>/"), recipe_list, name="category-detail"),
]
