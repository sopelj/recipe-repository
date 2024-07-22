from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Avg, Count
from inertia import inertia, render

from .models import Category, Recipe
from .serializers import CategoryListSerializer, RecipeListSerializer, RecipeSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@inertia("category-list")
def category_list(request: HttpRequest) -> HttpResponse:
    """List all available categories."""
    return render(
        request,
        "CategoryList",
        {"categories": CategoryListSerializer(Category.objects.all(), many=True).data},
    )


@inertia("recipe-list")
def recipe_list(request: HttpRequest) -> HttpResponse:
    """List all available recipes."""
    recipe_queryset = Recipe.objects.prefetch_related("categories").annotate(
        avg_rating=Avg("ratings__rating"),
        num_ratings=Count("ratings"),
    )

    return render(
        request,
        "RecipeList",
        {
            "recipes": RecipeListSerializer(recipe_queryset, many=True).data,
        },
    )


@inertia("recipe-detail")
def recipe_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Get a specific recipe by slug."""
    recipe = (
        Recipe.objects.prefetch_related("categories")
        .annotate(
            avg_rating=Avg("ratings__rating"),
            num_ratings=Count("ratings"),
        )
        .get(slug=slug)
    )
    return render(
        request,
        "RecipeDetail",
        {"recipe": RecipeSerializer(recipe).data},
    )
