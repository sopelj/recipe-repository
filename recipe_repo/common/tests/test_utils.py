from __future__ import annotations

from typing import Literal

import pytest
from django.utils import translation

from ..utils import pluralize, to_camel_case, to_snake_case


@pytest.mark.parametrize(
    ("count", "expected", "language"),
    [
        (0, "plural", "en"),
        (1, "singular", "en"),
        (5, "plural", "en"),
        (0, "singular", "fr"),
        (1, "singular", "fr"),
        (5, "plural", "fr"),
        (0, "singular", "ja"),
        (1, "singular", "ja"),
        (5, "singular", "ja"),
    ],
)
def test_pluralize(count: int, expected: str, language: Literal["en", "fr", "ja"]) -> None:
    with translation.override(language):
        assert pluralize("singular", "plural", count) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("test_test", "testTest"),
        ("test__test", "testTest"),
    ],
)
def test_to_camel_case(value: str, expected: str) -> None:
    assert to_camel_case(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("testTest", "test_test"),
        ("testTestA", "test_test_a"),
    ],
)
def test_to_snake_case(value: str, expected: str) -> None:
    assert to_snake_case(value) == expected
