from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, Q, Value
from django.http import Http404
from django.shortcuts import get_object_or_404
from inertia import inertia, render
from modeltranslation.utils import get_language

from .forms import ServingsForm
from .models import Category, Ingredient, Recipe
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@inertia("category-list")
def category_list(request: HttpRequest) -> HttpResponse:
    """List all available categories."""
    return render(
        request,
        "CategoryList",
        {"categories": CategoryListSerializer(Category.objects.all(), many=True).data},
    )


@login_required
@inertia("recipe-list")
def recipe_list(request: HttpRequest, category_slug: str | None = None) -> HttpResponse:
    """List all available recipes."""
    category: Category | None = None
    recipe_queryset = Recipe.objects.with_ratings().prefetch_related("categories")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipe_queryset = recipe_queryset.filter(categories__in=[category])
        categories = category.get_descendants()
    else:
        categories = Category.objects.filter()

    return render(
        request,
        "RecipeList",
        {
            "recipes": RecipeListSerializer(recipe_queryset, many=True).data,
            "category": CategorySerializer(category).data if category else None,
            "categories": CategorySerializer(categories, many=True).data,
        },
    )


def get_full_recipe(recipe_id: int) -> Recipe:
    """Ger the recipe with all necessary relationships."""
    return (
        Recipe.objects.with_ratings().select_related("source", "nutrition", "yield_unit", "added_by").get(pk=recipe_id)
    )


@inertia("recipe-detail")
def recipe_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Get a specific recipe by slug."""
    try:
        recipe_id, servings = Recipe.objects.values_list("pk", "servings").get(
            Q(**{f"slug_{get_language()}": slug}) | Q(slug_en=slug),
        )
    except Recipe.DoesNotExist as e:
        raise Http404("Recipe does not exist.") from e

    form = ServingsForm(request.GET, initial={"servings": servings})
    errors = None if form.is_valid() else form.errors

    scale = (form.cleaned_data.get("servings") or servings) / servings
    ingredients = (
        Ingredient.objects.filter(recipe_id=recipe_id)
        .annotate(scale=Value(scale or 1, output_field=DecimalField()))
        .select_related("unit", "food", "qualifier")
    )

    return render(
        request,
        "RecipeDetail",
        {
            "recipe": lambda: RecipeSerializer(get_full_recipe(recipe_id)).data,
            "servings": float((servings or 1) * scale),
            "ingredients": lambda: IngredientSerializer(ingredients, many=True).data,
            "errors": errors,
        },
    )
