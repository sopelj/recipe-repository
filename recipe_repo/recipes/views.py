from __future__ import annotations

import contextlib
from functools import cached_property
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DecimalField, Q, Value
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from modeltranslation.utils import get_language

from ..inertia.views import InertiaFormView, InertiaView
from .forms import RecipeReviewForm, ServingsForm
from .models import Category, Ingredient, Recipe
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
)


class CategoryListView(InertiaView, LoginRequiredMixin):
    component = "CategoryList"

    def get_component_props(self) -> dict[str, Any]:
        """Return categories."""
        return {
            "categories": CategoryListSerializer(Category.objects.filter(top_level=True), many=True).data,
        }


class RecipeListView(InertiaView, LoginRequiredMixin):
    component = "RecipeList"

    def get_component_props(self) -> dict[str, Any]:
        """Get all recipes or the recipes in the specified category."""
        category_slug = self.kwargs.get("category_slug", None)
        category: Category | None = None
        recipe_queryset = Recipe.objects.prefetch_related("categories").with_ratings()  # type: ignore[attr-defined]
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            recipe_queryset = recipe_queryset.filter(categories__in=[category])
            categories = category.sub_categories.all()
        else:
            categories = Category.objects.filter(top_level=True)

        return {
            "recipes": RecipeListSerializer(recipe_queryset, many=True).data,
            "category": CategorySerializer(category).data if category else None,
            "categories": CategorySerializer(categories, many=True).data,
        }


def get_full_recipe(recipe_id: int) -> Recipe:
    """Ger the recipe with all necessary relationships."""
    recipe: Recipe = (
        Recipe.objects.select_related(
            "source",
            "nutrition",
            "yield_unit",
            "added_by",
        )
        .with_ratings()  # type: ignore[attr-defined]
        .get(pk=recipe_id)
    )
    return recipe


class RecipeDetailView(InertiaFormView, SingleObjectMixin[Recipe]):
    component = "RecipeDetail"
    form_class = RecipeReviewForm

    @cached_property
    def id_and_servings(self) -> tuple[int, int | None]:
        """Fetch PK and servings from Recipe and 404 if no match found."""
        try:
            slug = self.kwargs["slug"]
            return Recipe.objects.values_list("pk", "servings").get(
                Q(**{f"slug_{get_language()}": slug}) | Q(slug_en=slug),
            )
        except Recipe.DoesNotExist as e:
            raise Http404("Recipe does not exist.") from e

    def get_user_rating(self) -> int | None:
        """Get the user's rating for the current recipe, if there is one."""
        recipe_id = self.id_and_servings[0]
        if self.request.user.is_authenticated:
            with contextlib.suppress(IndexError):
                return self.request.user.ratings.filter(recipe_id=recipe_id).values_list("rating", flat=True)[0]
        return None

    def get_component_props(self) -> dict[str, Any]:
        """Get props for RecipeDetail component."""
        recipe_id, servings = self.id_and_servings

        form = ServingsForm(self.request.GET, initial={"servings": servings})
        form.is_valid()
        scale = (form.cleaned_data.get("servings") or servings or 1) / (servings or 1)
        ingredients = (
            Ingredient.objects.filter(recipe_id=recipe_id)
            .annotate(scale=Value(scale or 1, output_field=DecimalField()))
            .select_related("unit", "food", "qualifier", "group")
            .order_by("group__order", "order")
        )
        return {
            "recipe": lambda: RecipeSerializer(get_full_recipe(recipe_id)).data,
            "servings": float((servings or 1) * scale),
            "ingredients": lambda: IngredientSerializer(ingredients, many=True).data,
            "userRating": self.get_user_rating(),
        }
