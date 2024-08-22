from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from recipe_repo.conftest import InertiaPageHelper

if TYPE_CHECKING:
    from django.test import Client

    from recipe_repo.recipes.models import Category, Recipe
    from recipe_repo.users.models import User


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["/en/", "/en/categories/"])
def test_recipe_and_category_list_not_logged_in(path: str, client: Client) -> None:
    resp = client.get(path)
    assert resp.status_code == 302
    assert resp.url == f"/en/admin/login/?next={path}"  # type: ignore[attr-defined]


@pytest.mark.django_db
def test_recipe_list_logged_in(recipe: Recipe, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper("/en/", client=client)
    assert inertia.component == "RecipeList"
    recipes = inertia.props["recipes"]
    assert len(recipes) == 1
    assert recipes[0]["name"] == recipe.name


@pytest.mark.django_db
def test_recipe_detail(recipe: Recipe) -> None:
    inertia = InertiaPageHelper(f"/en/recipes/{recipe.slug}/")
    assert inertia.component == "RecipeDetail"
    recipe_prop = inertia.props["recipe"]
    assert recipe_prop["name"] == recipe.name
    assert inertia.props["servings"] == 1.0


@pytest.mark.django_db
def test_category_list(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper("/en/categories/", client=client)
    assert inertia.component == "CategoryList"
    categories = inertia.props["categories"]
    assert categories[0]["name"] == category.name


@pytest.mark.django_db
def test_category_detail(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper(f"/en/categories/{category.slug}/", client=client)
    assert inertia.component == "RecipeList"
