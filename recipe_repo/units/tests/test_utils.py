from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest
from django.utils import translation

from ..utils import (
    CUP_FRACTIONS,
    TBSP_FRACTIONS,
    format_decimal_as_fraction,
    format_fraction,
    is_nice_fraction,
)

if TYPE_CHECKING:
    from ..utils import Fractions


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
def test_parse_numeric_string(language: str, whole: int, fraction: str, expected: str) -> None:
    with translation.override(language):
        assert format_fraction(whole, Fraction(fraction)) == expected


@pytest.mark.parametrize(
    ("language", "amount", "expected"),
    [
        ("en", Decimal(0.5), "1\u20442"),
        ("en", Decimal("1.33333333"), "1\u00a01\u20443"),
        ("en", Decimal(2.5), "2\u00a01\u20442"),
        ("ja", Decimal(0.5), "2分の1分"),
        ("ja", Decimal("1.33333333"), "1と3分の1分"),
        ("ja", Decimal(2.5), "2と2分の1分"),
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
        (Decimal("0.5"), CUP_FRACTIONS, True),
        (Decimal("1.33333333"), CUP_FRACTIONS, True),
        (Decimal("1.8888888"), CUP_FRACTIONS, False),
    ],
)
def test_is_nice_fraction(amount: Decimal, allowed: Fractions, expected: bool) -> None:
    assert is_nice_fraction(amount, allowed) == expected
