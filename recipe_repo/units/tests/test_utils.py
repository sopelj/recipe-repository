from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest
from django.utils import translation

from .. import unit_registry as ureg
from ..utils import (
    BASIC_FRACTIONS,
    TBSP_FRACTIONS,
    find_imperial_unit,
    format_decimal_as_fraction,
    format_fraction,
    format_imperial_amounts,
    is_nice_fraction,
    normalize_decimal,
    parse_numeric_string,
)

if TYPE_CHECKING:
    import pint

    from ..utils import Fractions


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
    ("numeric", "number"),
    [
        ("1.000", "1"),
        ("1.05", "1.05"),
        ("1.050", "1.05"),
    ],
)
def test_normalize_decimal(numeric: str, number: str) -> None:
    assert normalize_decimal(Decimal(numeric)) == Decimal(number)


@pytest.mark.parametrize(
    ("language", "whole", "fraction", "expected"),
    [
        ("en", 0, "1/2", "1\u20442"),
        ("en", 1, "1/3", "1\u00a01\u20443"),
        ("en", 2, "1/2", "2\u00a01\u20442"),
        ("ja", 0, "1/2", "2分の1分"),
        ("ja", 1, "1/3", "1と3分の1分"),
        ("ja", 2, "1/2", "2と2分の1分"),
    ],
)
def test_format_fraction(language: str, whole: int, fraction: str, expected: str) -> None:
    with translation.override(language):
        assert format_fraction(whole, Fraction(fraction)) == expected


@pytest.mark.parametrize(
    ("language", "amount", "expected"),
    [
        ("en", Decimal("0.5"), "1\u20442"),
        ("en", Decimal("1.33333333"), "1\u00a01\u20443"),
        ("en", Decimal("2.5"), "2\u00a01\u20442"),
        ("ja", Decimal("0.5"), "2分の1分"),
        ("ja", Decimal("1.33333333"), "1と3分の1分"),
        ("ja", Decimal("2.5"), "2と2分の1分"),
    ],
)
def test_format_decimal_as_fraction(language: str, amount: Decimal, expected: str) -> None:
    with translation.override(language):
        assert format_decimal_as_fraction(Decimal(amount)) == expected


@pytest.mark.parametrize(
    ("amount", "allowed", "expected"),
    [
        (Decimal("1.5"), TBSP_FRACTIONS, True),
        (Decimal("1.33333333"), TBSP_FRACTIONS, False),
        (Decimal("0.5"), BASIC_FRACTIONS, True),
        (Decimal("1.33333333"), BASIC_FRACTIONS, True),
        (Decimal("1.8888888"), BASIC_FRACTIONS, False),
    ],
)
def test_is_nice_fraction(amount: Decimal, allowed: Fractions, expected: bool) -> None:
    assert is_nice_fraction(amount, allowed) == expected


@pytest.mark.parametrize(
    ("quantity", "expected"),
    [
        (Decimal("1") * ureg.quart, (Decimal(1), "quart")),
        (Decimal("0.5") * ureg.quart, (Decimal(2), "cup")),
        (Decimal("2") * ureg.cups, (Decimal(2), "cup")),
        (Decimal("0.0208333333333") * ureg.cups, (Decimal(1), "teaspoon")),
        (Decimal("3") * ureg.tsp, (Decimal(1), "tablespoon")),
        (Decimal("0.25") * ureg.cups, (Decimal("0.25"), "cup")),
    ],
)
def test_find_imperial_unit(quantity: pint.Quantity[Decimal], expected: tuple[Decimal, str]) -> None:
    assert find_imperial_unit(quantity) == expected


@pytest.mark.parametrize(
    ("amount", "amount_max", "unit", "expected"),
    [
        (Decimal("1"), Decimal(3), ureg.tsp, ("1 tsp to 1 tbsp", Decimal(1))),
        (Decimal("1"), Decimal(2), ureg.tsp, ("1 to 2 tsp", Decimal(2))),
        (Decimal("1"), Decimal(2), ureg.quarts, ("1 to 2 quarts", Decimal(2))),
        (Decimal("1"), None, ureg.tsp, ("1 tsp", Decimal(1))),
    ],
)
def test_format_imperial_amounts(
    amount: Decimal,
    amount_max: Decimal,
    unit: pint.Unit,
    expected: tuple[str, Decimal],
) -> None:
    assert format_imperial_amounts(amount, amount_max, unit) == expected
