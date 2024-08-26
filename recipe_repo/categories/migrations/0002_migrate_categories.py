# Generated by Django 4.2.15 on 2024-08-25 19:42
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def migrate_recipe_categories(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    RecipeCategory = apps.get_model("recipes", "Category")
    CategoryType = apps.get_model("categories", "CategoryType")
    Category = apps.get_model("categories", "Category")

    for recipe_category in RecipeCategory.objects.filter(path__depth=1):
        category_type = CategoryType.objects.create(
            name=recipe_category.name,
            name_en=recipe_category.name_en,
            name_fr=recipe_category.name_fr,
            name_ja=recipe_category.name_ja,
            slug=recipe_category.slug,
            slug_en=recipe_category.slug_en,
            slug_fr=recipe_category.slug_fr,
            slug_ja=recipe_category.slug_ja,
            image=recipe_category.image,
        )
        category_type.save()
        for sub_category in RecipeCategory.objects.filter(path__descendants=recipe_category.path, path__depth=2):
            cat = Category.objects.create(
                name=sub_category.name,
                name_en=sub_category.name_en,
                name_fr=sub_category.name_fr,
                name_ja=sub_category.name_ja,
                slug=sub_category.slug,
                slug_en=sub_category.slug_en,
                slug_fr=sub_category.slug_fr,
                slug_ja=sub_category.slug_ja,
                image=sub_category.image,
                type=category_type,
            )
            cat.save()


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_recipe_categories, migrations.RunPython.noop),
    ]
