from django.http import HttpRequest, HttpResponse
from inertia import share


def inertia_share(get_response):
    """Middleware to inject shared data for inertia."""

    def middleware(request: HttpRequest) -> HttpResponse:
        """Add shared data for inertia."""
        share(request, user=lambda: request.user.serialize() if request.user.is_authenticated else None)
        return get_response(request)

    return middleware
