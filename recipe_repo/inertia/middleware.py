from django.conf import settings
from django.http import HttpRequest, HttpResponse
from inertia import share

from recipe_repo.users.serializers import UserSerializer


def inertia_share(get_response):
    """Middleware to inject shared data for inertia."""

    def middleware(request: HttpRequest) -> HttpResponse:
        """Add shared data for inertia."""
        share(
            request,
            user=lambda: UserSerializer(request.user).data if request.user.is_authenticated else None,
            locale=lambda: getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE),
        )
        return get_response(request)

    return middleware
