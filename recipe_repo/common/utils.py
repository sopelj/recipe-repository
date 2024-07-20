from __future__ import annotations

import re


def to_camel_case(snake: str) -> str:
    """Convert snake_case to camelCase."""
    parts = snake.split("_")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def to_snake_case(camel: str) -> str:
    """Convert camelCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()
