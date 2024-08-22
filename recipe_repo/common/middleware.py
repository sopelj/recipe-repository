from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.translation.trans_real import get_language
from inertia import share

from recipe_repo.users.serializers import UserSerializer

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest, HttpResponse


def inertia_share(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    """Middleware to inject shared data for inertia."""

    def middleware(request: HttpRequest) -> HttpResponse:
        current_language = get_language()
        """Add shared data for inertia."""
        share(
            request,
            user=lambda: UserSerializer(request.user).data if request.user.is_authenticated else None,
            locale=lambda: current_language,
            errors=lambda: request.session.pop("errors", {}),
        )
        return get_response(request)

    return middleware
