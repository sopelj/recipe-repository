from __future__ import annotations

from typing import Any

from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import DurationField, IntegerField, ModelSerializer, SlugRelatedField

from ..categories.serializers import CategorySerializer
from ..food.models import Food
from ..units.models import Unit
from ..users.serializers import CommentSerializer, UserSerializer
from .models import (
    Ingredient,
    IngredientGroup,
    IngredientQualifier,
    NutritionInformation,
    Recipe,
    Source,
    Step,
    YieldUnit,
)


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


class IngredientUpdateSerializer(ModelSerializer[Ingredient]):
    food_id = PrimaryKeyRelatedField(queryset=Food.objects.all())
    unit_id = PrimaryKeyRelatedField(queryset=Unit.objects.all())
    qualifier_id = PrimaryKeyRelatedField(queryset=IngredientQualifier.objects.all())
    group_id  = PrimaryKeyRelatedField(queryset=IngredientGroup.objects.all())

    class Meta:
        model = Ingredient
        fields = ("id", "amount", "amount_max", "food_id", "unit_id", "qualifier_id", "group_id", "optional", "note")


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


class StepUpdateSerializer(ModelSerializer[Step]):
    class Meta:
        model = Step
        fields = ("id", "text", "order")


class RecipeUpdateSerializer(ModelSerializer[Recipe]):
    ingredient_groups = IngredientGroupSerializer(many=True)
    steps = StepUpdateSerializer(many=True)
    ingredients = IngredientUpdateSerializer(many=True, write_only=True)

    _errors: dict[str, Any]

    def save(self, **kwargs: Any) -> Recipe:
        """Save recipe and nested serializers."""
        ingredient_groups_data = self.validated_data.pop("ingredient_groups", [])
        steps_data = self.validated_data.pop("steps", [])
        ingredients_data = self.validated_data.pop("ingredients", [])

        recipe = super().save(**kwargs)

        self._save_nested(recipe, "ingredient_groups", IngredientGroupSerializer, ingredient_groups_data)
        self._save_nested(recipe, "steps", StepUpdateSerializer, steps_data)
        self._save_nested(recipe, "ingredients", IngredientUpdateSerializer, ingredients_data)

        return recipe

    def _save_nested(
        self,
        recipe: Recipe,
        field_name: str,
        serializer_class: type[IngredientGroupSerializer | StepUpdateSerializer |IngredientUpdateSerializer],
        data: list[dict[str, Any]],
    ) -> None:
        """Save nested data and handle errors."""
        existing_objects = {obj.pk: obj for obj in getattr(recipe, field_name).all()}
        new_objects_pks: list[int] = []
        errors: list[dict[str, Any]] = []
        has_errors = False

        for item_data in data:
            pk = item_data.get("id")
            instance = existing_objects.get(pk)
            serializer = serializer_class(instance, data=item_data, partial=True)
            if serializer.is_valid():
                obj = serializer.save(recipe=recipe)
                new_objects_pks.append(obj.pk)
                errors.append({})
            else:
                errors.append(serializer.errors)
                has_errors = True

        if has_errors:
            self._errors[field_name] = errors

        # Delete objects not in the new data
        getattr(recipe, field_name).exclude(pk__in=new_objects_pks).delete()

    class Meta:
        model = Recipe
        fields = (
            "name",
            "description",
            "cook_time",
            "prep_time",
            "ingredient_groups",
            "steps",
            "ingredients",
        )

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
