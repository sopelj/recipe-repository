from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

type FracTuple = tuple[int, int]
type Fractions = tuple[FracTuple, ...]
type SplitFractions = tuple[Decimal, FracTuple | None, Decimal]

FRACTIONS_PER_IMPERIAL_UNIT: dict[str, Fractions] = {
    "cup": ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4)),
    "tbsp": ((1, 2),),
    "tsp": ((1, 2), (1, 4), (1, 8)),
}


def split_unit_fraction(amount: Decimal, allowed_fractions: Fractions) -> SplitFractions:
    """Return whole, fraction based on allowed_fractions, and remainder."""
    base = amount.to_integral()
    fraction = None
    if remainder := amount - base:
        fraction = Fraction(remainder).limit_denominator(1_000).as_integer_ratio()
        if fraction and allowed_fractions and fraction not in allowed_fractions:
            return base, None, remainder
    return base, fraction, Decimal(0)
