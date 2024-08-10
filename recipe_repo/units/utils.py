from __future__ import annotations

import re
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING
from unicodedata import numeric

from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from recipe_repo.common.utils import pluralize

if TYPE_CHECKING:
    from typing import TypeAlias

    from pint.facets.plain.quantity import PlainQuantity

    FracTuple: TypeAlias = tuple[int, int]  # noqa UP040
    Fractions: TypeAlias = tuple[FracTuple, ...]  # noqa UP040
    SplitFractions: TypeAlias = tuple[Decimal, FracTuple | None, Decimal]  # noqa UP040
    DecimalQuantity: TypeAlias = PlainQuantity[Decimal]  # noqa UP040

NUMERIC_STRING_REGEX = re.compile(r"(([0-9]*\s?)?(([0-9]+/[0-9]+)|([\u2150-\u215E\u00BC-\u00BE])))|([0-9]+)")

TSP_FRACTIONS = ((1, 2), (1, 4), (1, 8))
TBSP_FRACTIONS = ((1, 2),)
BASIC_FRACTIONS = ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4))

FRACTIONS_PER_IMPERIAL_UNIT: dict[str, Fractions] = {
    "cup": BASIC_FRACTIONS,
    "tablespoon": TBSP_FRACTIONS,
    "teaspoon": TSP_FRACTIONS,
    "pound": BASIC_FRACTIONS,
    "ounce": BASIC_FRACTIONS,
}
IMPERIAL_UNITS_VOLUME = ("cup", "tablespoon", "teaspoon")
IMPERIAL_UNITS_WEIGHT = ("pound", "ounce")
IMPERIAL_LABELS = {
    "teaspoon": (_("tsp"), None),
    "tablespoon": (_("tbsp"), None),
    "cup": (_("cup"), _("cups")),
    "pint": (_("pint"), _("pints")),
    "quart": (_("quart"), _("quarts")),
    "ounce": (_("oz"), None),
    "fluid_ounce": (_("fl oz"), None),
    "pound": (_("lb"), None),
}


def parse_numeric_string(value: str) -> Decimal | None:
    """Attempt to parse a string that could be an int or fraction into a decimal."""
    if not (match := NUMERIC_STRING_REGEX.match(value.strip(" "))):
        return None
    whole, __, fraction, fake_fraction, only_num = match.groups()[1:]
    amount: float = int(num) if (num := only_num or whole) else 0
    if fraction and (f := Fraction(fraction)):
        amount += f.numerator / f.denominator
    elif fake_fraction:
        amount += numeric(fake_fraction)
    return Decimal(amount)


def soft_round(value: Decimal) -> Decimal:
    """
    Slightly round a decimal and remove trailing zeros.

    We round to the last decimal place to avoid 0.9999999 != 1
    TODO: validate decimal places to keep and impacts
    """
    return value.quantize(Decimal("1.00000")).normalize()


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


def decimal_to_fraction(amount: Decimal, limit: int = 10_000) -> tuple[Decimal, Fraction | None]:
    """Split decimal into whole number and fraction."""
    amount = soft_round(amount)
    whole = Decimal(int(amount))
    frac = Fraction(remainder).limit_denominator(limit) if (remainder := amount - whole) else None
    return whole, frac


def is_nice_fraction(amount: Decimal, allowed_fractions: Fractions) -> bool:
    """Check if a given amount is a nice fraction."""
    fraction = decimal_to_fraction(amount)[1]
    return not fraction or fraction.as_integer_ratio() in allowed_fractions


def find_imperial_unit(quantity: DecimalQuantity) -> tuple[Decimal, str]:
    """Find the best imperial unit for displaying this quantity."""
    units: tuple[str, ...] = IMPERIAL_UNITS_VOLUME
    if not quantity.units.is_compatible_with("cup"):
        units = IMPERIAL_UNITS_WEIGHT

    current_unit = str(quantity.units)
    if current_unit not in units and not decimal_to_fraction(quantity.magnitude)[1]:
        return soft_round(quantity.magnitude), current_unit
    for new_unit in units:
        new_unit_quantity = quantity.to(new_unit)
        if is_nice_fraction(new_unit_quantity.magnitude, FRACTIONS_PER_IMPERIAL_UNIT.get(new_unit, ())):
            quantity = new_unit_quantity
            break
        if not decimal_to_fraction(new_unit_quantity.magnitude)[1]:
            quantity = new_unit_quantity
            break
    return soft_round(quantity.magnitude), str(quantity.units)


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


def format_metric_amounts(amount: Decimal, max_amount: Decimal | None, unit: DecimalQuantity) -> tuple[str, Decimal]:
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


def format_imperial_amount(amount: Decimal, unit: str | None) -> str:
    """Return a single unit formatted for display with unit if provided."""
    formatted_amount = format_decimal_as_fraction(amount)
    if unit:
        name, name_plural = IMPERIAL_LABELS.get(unit, (unit, None))
        return gettext("{amount} {unit}").format(amount=formatted_amount, unit=pluralize(name, name_plural, amount))
    return formatted_amount


def format_imperial_amounts(amount: Decimal, max_amount: Decimal | None, unit: DecimalQuantity) -> tuple[str, Decimal]:
    """Format amounts for imperial units."""
    new_amount, new_unit = find_imperial_unit(amount * unit)
    if max_amount:
        new_amount_max, new_amount_max_unit = find_imperial_unit(max_amount * unit)
        return (
            gettext("{amount} to {max_amount}").format(
                amount=format_imperial_amount(amount, new_unit if new_unit != new_amount_max_unit else None),
                max_amount=format_imperial_amount(new_amount_max, new_amount_max_unit),
            ),
            new_amount_max,
        )
    return format_imperial_amount(new_amount, new_unit), new_amount
