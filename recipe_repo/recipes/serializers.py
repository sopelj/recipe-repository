from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.serializers import DurationField, IntegerField, ModelSerializer, SlugRelatedField

from ..users.serializers import UserSerializer
from .models import Category, Ingredient, NutritionInformation, Recipe, Source

if TYPE_CHECKING:
    from .models import IngredientQualifier, Step, YieldUnit


class CategorySerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug")


class CategoryListSerializer(ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug", "thumbnail_image_url")


class NutritionSerializer(ModelSerializer[NutritionInformation]):
    class Meta:
        model = NutritionInformation
        exclude = ("recipe", "id")


class SourceSerializer(ModelSerializer[Source]):
    class Meta:
        model = Source
        fields = ("name", "type", "value")


class IngredientSerializer(ModelSerializer[Ingredient]):
    qualifier: SlugRelatedField[IngredientQualifier] = SlugRelatedField(read_only=True, slug_field="title")
    group_id = IntegerField()

    class Meta:
        model = Ingredient
        fields = ("id", "amount_display", "food_display", "optional", "note", "qualifier", "group_id")


class RecipeListSerializer(ModelSerializer[Recipe]):
    num_ratings = IntegerField()
    avg_rating = IntegerField(allow_null=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ("name", "slug", "thumbnail_url", "description", "categories", "num_ratings", "avg_rating")


class RecipeSerializer(RecipeListSerializer):
    total_time = DurationField()
    yield_unit: SlugRelatedField[YieldUnit] = SlugRelatedField(read_only=True, slug_field="name")
    steps: SlugRelatedField[Step] = SlugRelatedField(many=True, read_only=True, slug_field="text")
    source = SourceSerializer(read_only=True)  # type: ignore[assignment]
    nutrition = NutritionSerializer(read_only=True)
    added_by = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "name",
            "slug",
            "image_url",
            "description",
            "categories",
            "cook_time",
            "prep_time",
            "total_time",
            "nutrition",
            "num_ratings",
            "avg_rating",
            "steps",
            "source",
            "source_value",
            "servings",
            "yield_unit",
            "yield_amount",
            "added_by",
        )
