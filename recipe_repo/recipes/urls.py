from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import CategoryListView, RecipeDetailView, RecipeListView

app_name = "recipes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe-list"),
    path(_("recipes/<slug:slug>/"), RecipeDetailView.as_view(), name="recipe-detail"),
    path(_("categories/"), CategoryListView.as_view(), name="category-list"),
    path(_("categories/<slug:category_slug>/"), RecipeListView.as_view(), name="category-detail"),
]
