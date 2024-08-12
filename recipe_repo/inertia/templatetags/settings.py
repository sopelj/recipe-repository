from __future__ import annotations

from typing import Any

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_setting[T](name: str, fallback: T = None) -> T | None | Any:  # type: ignore[valid-type,name-defined]
    """Get a setting by name in the template."""
    return getattr(settings, name, fallback)
