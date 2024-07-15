from django.db.models import QuerySet
from django.http import HttpRequest
from inertia import inertia, render

from .models import Category


@inertia("index")
def categories(request: HttpRequest) -> dict[str, QuerySet]:
    """List all available categories."""
    return render(
        request,
        "index",
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
