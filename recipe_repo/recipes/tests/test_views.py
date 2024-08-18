from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from recipe_repo.conftest import InertiaPageHelper

if TYPE_CHECKING:
    from recipe_repo.recipes.models import Category, Recipe


@pytest.mark.django_db
def test_recipe_list(recipe: Recipe) -> None:
    inertia = InertiaPageHelper("/en/")
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
def test_category_list(category: Category) -> None:
    inertia = InertiaPageHelper("/en/categories/")
    assert inertia.component == "CategoryList"
    categories = inertia.props["categories"]
    assert categories[0]["name"] == category.name


@pytest.mark.django_db
def test_category_detail(category: Category) -> None:
    inertia = InertiaPageHelper(f"/en/categories/{category.slug}/")
    assert inertia.component == "RecipeList"
