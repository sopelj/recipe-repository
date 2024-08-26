from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..recipes.views import RecipeListView
from .views import CategoryListView, CategoryTypeListView

app_name = "categories"

urlpatterns = [
    path(_("category-types/"), CategoryTypeListView.as_view(), name="category-type-list"),
    path(_("category-types/<slug:category_type_slug>/"), CategoryListView.as_view(), name="category-type-detail"),
    path(_("categories/<slug:category_slug>/"), RecipeListView.as_view(), name="category-recipe-list"),
]
