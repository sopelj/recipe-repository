from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import RecipeDetailView, RecipeEditView, RecipeImportView, RecipeListView

app_name = "recipes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe-list"),
    path(_("recipes/import/"), RecipeImportView.as_view(), name="recipe-import"),
    path(_("recipes/add/"), RecipeEditView.as_view(), name="recipe-add"),
    path(_("recipes/<str:slug>/"), RecipeDetailView.as_view(), name="recipe-detail"),
    path(_("recipes/<str:slug>/edit/"), RecipeEditView.as_view(), name="recipe-edit"),
]
