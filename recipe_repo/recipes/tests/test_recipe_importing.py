from __future__ import annotations

import pytest

from ..recipe_importing import extract_notes


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("potatoes", ("potatoes", "")),
        ("2 eggs or 1 banana ", ("2 eggs", "or 1 banana")),
        ("neutral oil (for cooking)", ("neutral oil", "for cooking")),
    ],
)
def test_extract_notes(text: str, expected: tuple[str, str]) -> None:
    assert extract_notes(text) == expected
