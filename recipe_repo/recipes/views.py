from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Avg, Count, Q, QuerySet
from django.shortcuts import get_object_or_404
from inertia import inertia, render
from modeltranslation.utils import get_language

from .models import Category, Recipe
from .serializers import CategoryListSerializer, CategorySerializer, RecipeListSerializer, RecipeSerializer

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
def recipe_list(request: HttpRequest, category_slug: str | None = None) -> HttpResponse:
    """List all available recipes."""
    category: Category | None = None
    parent_categories: QuerySet[Category] | None = None
    recipe_queryset = Recipe.objects.prefetch_related("categories").annotate(
        avg_rating=Avg("ratings__rating"),
        num_ratings=Count("ratings"),
    )
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipe_queryset = recipe_queryset.filter(categories__in=[category])
        parent_categories = category.get_ancestors()

    return render(
        request,
        "RecipeList",
        {
            "recipes": RecipeListSerializer(recipe_queryset, many=True).data,
            "category": CategorySerializer(category).data if category else None,
            "parentCategories": CategorySerializer(parent_categories, many=True).data if parent_categories else None,
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
        .get(Q(**{f"slug_{get_language()}": slug}) | Q(slug_en=slug))
    )
    return render(
        request,
        "RecipeDetail",
        {"recipe": RecipeSerializer(recipe).data},
    )
