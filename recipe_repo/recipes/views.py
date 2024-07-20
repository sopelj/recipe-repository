from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Avg, Count
from django.forms import model_to_dict
from easy_thumbnails.files import get_thumbnailer
from inertia import inertia, render

from .models import Category, Recipe

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@inertia("category-list")
def category_list(request: HttpRequest) -> HttpResponse:
    """List all available categories."""
    return render(
        request,
        "CategoryList",
        {
            "categories": [
                {
                    "name": category.name,
                    "name_plural": category.name_plural,
                    "slug": category.slug,
                    "thumbnail_image_url": category.thumbnail_image_url,
                }
                for category in Category.objects.all()
            ],
        },
    )


@inertia("recipe-list")
def recipe_list(request: HttpRequest) -> HttpResponse:
    """List all available recipes."""
    return render(
        request,
        "RecipeList",
        {
            "recipes": [
                recipe
                | {
                    "thumbnail_url": (
                        get_thumbnailer(image_url)["thumbnail"].url if (image_url := recipe["image"]) else None
                    ),
                }
                for recipe in Recipe.objects.prefetch_related("categories")
                .annotate(
                    avg_rating=Avg("ratings__rating"),
                    num_ratings=Count("ratings"),
                )
                .values("name", "slug", "image", "categories", "avg_rating", "num_ratings")
            ],
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
        {"recipe": model_to_dict(recipe, exclude="image")},
    )
