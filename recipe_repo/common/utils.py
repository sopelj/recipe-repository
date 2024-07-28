from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django.utils.translation import get_language

if TYPE_CHECKING:
    from decimal import Decimal


def pluralize(singular: str, plural: str | None, count: Decimal | float) -> str:
    """Return the plural or singular form depending on language and count."""
    if not plural:  # no point checking
        return singular
    match get_language():
        case "en":
            return singular if count == 1 else plural
        case "fr":
            return plural if count > 1 else (plural or singular)
        case _:
            return singular


def to_camel_case(snake: str) -> str:
    """Convert snake_case to camelCase."""
    parts = snake.split("_")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def to_snake_case(camel: str) -> str:
    """Convert camelCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()
