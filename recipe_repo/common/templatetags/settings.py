from __future__ import annotations

from typing import Any

from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def get_setting[T](name: str, fallback: T | None = None) -> T | None | Any:
    """Get a setting by name in the template."""
    return getattr(settings, name, fallback)


@register.simple_tag()
def include_umami_script() -> str:
    """Include umami script tag if settings are defined."""
    print(settings.UMAMI_SITE_ID, settings.UMAMI_URL)
    if settings.UMAMI_SITE_ID and settings.UMAMI_URL:
        return format_html(
            '<script defer src="{}/script.js" data-website-id="{}"></script>',
            settings.UMAMI_URL,
            settings.UMAMI_SITE_ID,
        )
    return ""
