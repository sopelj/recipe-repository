from __future__ import annotations

from typing import TYPE_CHECKING

from inertia import inertia, render

from .models import Category

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
