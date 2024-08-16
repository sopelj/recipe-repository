from __future__ import annotations

from functools import cached_property
from json import loads
from typing import TYPE_CHECKING, TypedDict, cast
from unittest.mock import patch

import pytest
from django.db import transaction
from django.shortcuts import render
from django.test import Client

from .recipes.models import Category, Recipe

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

    from django.http import HttpResponse


class InertiaPageResponse(TypedDict):
    props: dict[str, Any]
    component: str
    url: str
    version: str


class InertiaPageHelper:
    """Helper for fetching Inertia pages based on django-inertia test utils."""

    response: HttpResponse

    def __init__(self, url: str, method: str = "get", data: dict[str, Any] | None = None, client: Client | None = None):
        """Perform the request using the test client, and store the response."""
        self._method = method
        self._url = url
        self.client = client if client else Client()
        with patch("inertia.http.base_render", wraps=render) as mock_render:
            self.response = getattr(self.client, method)(url, json=data)
            self.mock_render = mock_render

    def __str__(self) -> str:
        """Display some information about the request when coerced to string for debugging."""
        return f"[{self._method.upper()}] {self.response.status_code}: {self._url}"

    def __repr__(self) -> str:
        """Display some basic information in test logs for debugging."""
        return f"InertiaHelper<{self}>"

    @cached_property
    def component(self) -> str:
        """Get the component name from the response."""
        return self.page["component"]

    @cached_property
    def props(self) -> dict[str, Any]:
        """Get the props from the response."""
        return self.page["props"]

    @cached_property
    def page(self) -> InertiaPageResponse:
        """Extract the page information from the mocked request."""
        return cast(InertiaPageResponse, loads(self.mock_render.call_args.args[2]["page"]))


@pytest.fixture()
def inertia_client() -> Client:
    """Return a test client with the inertia headers."""
    return Client(HTTP_X_INERTIA=True)


@pytest.fixture(name="category")
def category_fixture() -> Generator[Category, None, None]:
    """Create a single basic category for the given test."""
    with transaction.atomic():
        category_instance = Category.objects.create(slug_en="test-category", name_en="Test Category", top_level=True)
        yield category_instance
        category_instance.delete()


@pytest.fixture(name="recipe")
def recipe_fixture() -> Generator[Recipe, None, None]:
    """Create a single basic recipe for the given test."""
    with transaction.atomic():
        recipe_instance = Recipe.objects.create(slug_en="rest-recipe", name_en="Test Recipe")
        yield recipe_instance
        recipe_instance.delete()
