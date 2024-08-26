from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from recipe_repo.conftest import InertiaPageHelper

if TYPE_CHECKING:
    from django.test import Client

    from recipe_repo.categories.models import Category
    from recipe_repo.users.models import User


@pytest.mark.django_db
def test_category_list(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper("/en/category-types/", client=client)
    assert inertia.component == "CategoryTypeList"
    category_types = inertia.props["categoryTypes"]
    assert category_types[0]["name"] == category.type.name


@pytest.mark.django_db
def test_category_type_detail(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
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
