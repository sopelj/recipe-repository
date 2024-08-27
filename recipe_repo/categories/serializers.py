from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from .models import Category, CategoryType


class CategoryTypeSerializer(ModelSerializer[CategoryType]):
    class Meta:
        model = CategoryType
        fields = ("name", "name_plural", "slug")


class CategoryTypeListSerializer(ModelSerializer[CategoryType]):
    class Meta:
        model = CategoryType
        fields = ("name", "name_plural", "slug", "thumbnail_url")


class BaseCategorySerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug")


class CategoryListSerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug", "thumbnail_url")


class CategorySerializer(ModelSerializer[Category]):
    type = CategoryTypeSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug", "type")
