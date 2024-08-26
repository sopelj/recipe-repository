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
    inertia = InertiaPageHelper("/en/categories/", client=client)
    assert inertia.component == "CategoryTypeList"
    categories = inertia.props["categoryTypes"]
    assert categories[0]["name"] == category.type.name


@pytest.mark.django_db
def test_category_detail(category: Category, client: Client, user: User) -> None:
    client.force_login(user)
    inertia = InertiaPageHelper(f"/en/categories/{category.type.slug}/", client=client)
    assert inertia.component == "CategoryList"
