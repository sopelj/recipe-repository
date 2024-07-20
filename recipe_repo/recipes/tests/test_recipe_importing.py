from decimal import Decimal

import pytest

from ..recipe_importing import extract_notes, parse_numeric_string


@pytest.mark.parametrize(
    ("numeric", "number"),
    [
        ("1", 1),
        ("1/2", 0.5),
        ("2/3", 0.666),
        ("1 3/4", 1.75),
        ("2 3/4", 2.75),
        ("1 ¼", 1.25),
    ],
)
def test_parse_numeric_string(numeric: str, number: float) -> None:
    assert pytest.approx(parse_numeric_string(numeric), rel=Decimal("1e-3")) == Decimal(number)


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
