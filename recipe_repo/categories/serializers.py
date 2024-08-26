from __future__ import annotations

from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Category, CategoryType


class CategoryTypeSerializer(ModelSerializer[CategoryType]):
    class Meta:
        model = CategoryType
        fields = ("name", "name_plural", "slug")


class CategoryTypeListSerializer(ModelSerializer[CategoryType]):
    class Meta:
        model = CategoryType
        fields = ("name", "name_plural", "slug", "thumbnail_image_url")


class CategorySerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug")


class CategoryListSerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug", "thumbnail_image_url")


class CategoryTagSerializer(ModelSerializer[Category]):
    type = SlugRelatedField[CategoryType](slug_field="name", read_only=True)

    class Meta:
        model = Category
        fields = ("name", "type")
