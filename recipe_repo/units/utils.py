from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from django.utils.translation import gettext

if TYPE_CHECKING:
    from pint import Unit as PintUnit


type FracTuple = tuple[int, int]
type Fractions = tuple[FracTuple, ...]
type SplitFractions = tuple[Decimal, FracTuple | None, Decimal]


FRACTIONS_PER_IMPERIAL_UNIT: dict[str, Fractions] = {
    "cup": ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4)),
    "tbsp": ((1, 2),),
    "tsp": ((1, 2), (1, 4), (1, 8)),
}


def format_fraction(whole: Decimal | int, frac: Fraction) -> str:
    """Format a fraction localised for display."""
    if whole:
        return gettext("{whole} {numerator}⁄{denominator}").format(  # noqa: RUF001
            whole=whole,
            numerator=frac.numerator,
            denominator=frac.denominator,
        )
    return gettext("{numerator}⁄{denominator}").format(  # noqa: RUF001
        numerator=frac.numerator,
        denominator=frac.denominator,
    )


def format_decimal_as_fraction(amount: Decimal) -> str:
    """Format a decimal number as a fraction."""
    whole, fraction = decimal_to_fraction(amount)
    if fraction:
        return format_fraction(whole, fraction)
    return str(whole)


def decimal_to_fraction(amount: Decimal, limit: int = 1_000) -> tuple[Decimal, Fraction | None]:
    """Split decimal into whole number and fraction."""
    whole = amount.to_integral()
    frac = Fraction(remainder).limit_denominator(limit) if (remainder := amount - whole) else None
    return whole, frac


def is_nice_fraction(amount: Decimal, allowed_fractions: Fractions) -> bool:
    """Check if a given amount is a nice fraction."""
    base, fraction = decimal_to_fraction(amount)
    return fraction and fraction.as_integer_ratio() in allowed_fractions


def format_fraction_amounts(amount: Decimal, max_amount: Decimal | None) -> tuple[str, Decimal]:
    """Format amounts as a fraction or range of fractions."""
    if max_amount:
        return (
            gettext("{amount} to {max_amount}").format(
                amount=format_decimal_as_fraction(amount),
                max_amount=format_decimal_as_fraction(max_amount),
            ),
            max_amount,
        )
    return format_decimal_as_fraction(amount), amount


def format_metric_amounts(amount: Decimal, max_amount: Decimal | None, unit: PintUnit) -> tuple[str, Decimal]:
    """Format metric amounts as needed."""
    compact_amount = (amount * unit).to_compact()
    if compact_amount.magnitude < 0.0001:
        return gettext("a pinch"), Decimal(1)
    if max_amount:
        compact_max = (max_amount * unit).to_compact()
        return (
            gettext("{amount} to {max_amount}").format(
                amount=compact_amount.magnitude if compact_amount.unit == compact_max.unit else compact_amount,
                max_amount=compact_max,
            ),
            compact_max.magnitude,
        )
    return f"{compact_amount:~P}", compact_amount.magnitude
