from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.serializers import DurationField, IntegerField, ModelSerializer, SlugRelatedField

from ..categories.serializers import CategorySerializer
from ..users.serializers import CommentSerializer, UserSerializer
from .models import Ingredient, IngredientGroup, NutritionInformation, Recipe, Source, YieldUnit

if TYPE_CHECKING:
    from .models import IngredientQualifier, Step


class NutritionSerializer(ModelSerializer[NutritionInformation]):
    class Meta:
        model = NutritionInformation
        exclude = ("recipe", "id")


class SourceSerializer(ModelSerializer[Source]):
    class Meta:
        model = Source
        fields = ("name", "type", "value")


class YieldUnitSerializer(ModelSerializer[YieldUnit]):
    class Meta:
        model = YieldUnit
        fields = ("name", "name_plural")


class IngredientSerializer(ModelSerializer[Ingredient]):
    qualifier: SlugRelatedField[IngredientQualifier] = SlugRelatedField(read_only=True, slug_field="title")
    group_id = IntegerField()

    class Meta:
        model = Ingredient
        fields = ("id", "amount_display", "food_display", "optional", "note", "qualifier", "group_id")


class IngredientGroupSerializer(ModelSerializer[IngredientGroup]):
    class Meta:
        model = IngredientGroup
        fields = ("id", "name")


class RecipeListSerializer(ModelSerializer[Recipe]):
    num_ratings = IntegerField()
    avg_rating = IntegerField(allow_null=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ("name", "slug", "thumbnail_url", "description", "categories", "num_ratings", "avg_rating")


class RelatedRecipeSerializer(ModelSerializer[Recipe]):
    class Meta:
        model = Recipe
        fields = ("name", "slug")


class RecipeSerializer(RecipeListSerializer):
    total_time = DurationField()
    steps: SlugRelatedField[Step] = SlugRelatedField(many=True, read_only=True, slug_field="text")
    source = SourceSerializer(read_only=True)  # type: ignore[assignment]
    parent_recipes = RelatedRecipeSerializer(many=True, read_only=True)
    ingredient_groups = IngredientGroupSerializer(many=True, read_only=True)
    yield_unit = YieldUnitSerializer(read_only=True)
    nutrition = NutritionSerializer(read_only=True)
    added_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

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
            "ingredient_groups",
            "parent_recipes",
            "steps",
            "source",
            "source_value",
            "servings",
            "yield_unit",
            "yield_amount",
            "added_by",
            "comments",
        )
