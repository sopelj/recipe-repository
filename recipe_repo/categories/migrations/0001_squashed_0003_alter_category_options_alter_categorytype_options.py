# Generated by Django 4.2.15 on 2024-08-30 02:00

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    replaces = [
        ("categories", "0001_initial"),
        ("categories", "0002_migrate_categories"),
        ("categories", "0003_alter_category_options_alter_categorytype_options"),
    ]

    initial = True

    dependencies = [
        ("recipes", "0001_squashed_0014_alter_category_name_alter_category_name_en_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Name")),
                ("name_en", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_fr", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_ja", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_plural", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_en", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_fr", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_ja", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                (
                    "slug",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_en",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_fr",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_ja",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        blank=True,
                        null=True,
                        upload_to="images/categories/",
                        verbose_name="Thumbnail",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category Type",
                "verbose_name_plural": "Category types",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Name")),
                ("name_en", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_fr", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_ja", models.CharField(max_length=150, null=True, verbose_name="Name")),
                ("name_plural", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_en", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_fr", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                ("name_plural_ja", models.CharField(blank=True, max_length=150, null=True, verbose_name="Plural Name")),
                (
                    "slug",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_en",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_fr",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "slug_ja",
                    models.SlugField(
                        help_text="Automatically generated from the name",
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        blank=True,
                        null=True,
                        upload_to="images/categories/",
                        verbose_name="Thumbnail",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        to="categories.categorytype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("name",), "verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="categorytype",
            options={"ordering": ("name",), "verbose_name": "Category Type", "verbose_name_plural": "Category types"},
        ),
    ]
