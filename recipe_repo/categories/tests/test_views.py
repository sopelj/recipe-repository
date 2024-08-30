from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from recipe_repo.conftest import InertiaPageHelper

if TYPE_CHECKING:
    from django.test import Client

    from recipe_repo.categories.models import Category
    from recipe_repo.recipes.models import Recipe
    from recipe_repo.users.models import User


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["/en/category-types/", "/en/category-types/test-type/"])
def test_category_not_logged_in(path: str, client: Client) -> None:
    resp = client.get(path)
    assert resp.status_code == 302
    assert resp.url == f"/en/admin/login/?next={path}"  # type: ignore[attr-defined]


@pytest.mark.django_db
def test_category_list(category: Category, recipe: Recipe, client: Client, user: User) -> None:
    client.force_login(user)
    recipe.categories.add(category)
    inertia = InertiaPageHelper("/en/category-types/", client=client)
    assert inertia.component == "CategoryTypeList"
    category_types = inertia.props["categoryTypes"]
    assert category_types[0]["name"] == category.type.name


@pytest.mark.django_db
def test_category_type_detail(category: Category, recipe: Recipe, client: Client, user: User) -> None:
    client.force_login(user)
    recipe.categories.add(category)
    inertia = InertiaPageHelper(f"/en/category-types/{category.type.slug}/", client=client)
    assert inertia.component == "CategoryList"
    assert inertia.props["categoryType"]["name"] == category.type.name
    categories = inertia.props["categories"]
    assert categories[0]["name"] == category.name


@pytest.mark.django_db
def test_category_detail(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper(f"/en/categories/{category.slug}/", client=client)
    assert inertia.component == "RecipeList"
