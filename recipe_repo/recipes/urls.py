from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import RecipeDetailView, RecipeListView

app_name = "recipes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe-list"),
    path(_("recipes/<slug:slug>/"), RecipeDetailView.as_view(), name="recipe-detail"),
]
