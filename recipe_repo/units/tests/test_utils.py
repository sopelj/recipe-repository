from fractions import Fraction

import pytest
from django.utils import translation

from ..utils import format_fraction


@pytest.mark.parametrize(
    ("whole", "fraction", "language", "expected"),
    [
        (0, "1/2", "en", "1\u20442"),
        (1, "1/3", "en", "1\u00a01\u20443"),
        (2, "1/2", "en", "2\u00a01\u20442"),
        (0, "1/2", "ja", "2分の1分"),
        (1, "1/3", "ja", "1と3分の1分"),
        (2, "1/2", "ja", "2と2分の1分"),
    ],
)
def test_parse_numeric_string(whole: int, fraction: str, language: str, expected: str) -> None:
    with translation.override(language):
        assert format_fraction(whole, Fraction(fraction)) == expected
        print(format_fraction(whole, Fraction(fraction)))
