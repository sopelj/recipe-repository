from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rest_framework.fields import BooleanField, SlugField
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

if TYPE_CHECKING:
    RelatedSerializers = type["IngredientGroupSerializer" | "StepUpdateSerializer" | "IngredientUpdateSerializer"]


class NewIdField(IntegerField):
    def __init__(self, **kwargs: Any) -> None:
        """Ensure field is writable."""
        kwargs |= {"required": False, "allow_null": True}
        super().__init__(**kwargs)


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
    id = NewIdField()
    deleted = BooleanField(default=False, write_only=True, required=False)

    food = PrimaryKeyRelatedField(queryset=Food.objects.all())
    unit = PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False, allow_null=True)
    qualifier = PrimaryKeyRelatedField(queryset=IngredientQualifier.objects.all(), required=False, allow_null=True)
    group  = PrimaryKeyRelatedField(queryset=IngredientGroup.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "order",
            "amount",
            "amount_max",
            "food",
            "unit",
            "qualifier",
            "group",
            "optional",
            "note",
            "deleted",
        )


class IngredientGroupSerializer(ModelSerializer[IngredientGroup]):
    id = NewIdField()

    class Meta:
        model = IngredientGroup
        fields: tuple[str, ...] = ("id", "order", "name")


class IngredientGroupUpdateSerializer(IngredientGroupSerializer):
    id = NewIdField()
    deleted = BooleanField(default=False, write_only=True, required=False)

    class Meta(IngredientGroupSerializer.Meta):
        fields = ("id", "order", "name", "deleted")


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
    id = NewIdField()
    deleted = BooleanField(default=False, write_only=True, required=False)

    class Meta:
        model = Step
        fields = ("id", "text", "order", "deleted")


class RecipeUpdateSerializer(ModelSerializer[Recipe]):
    id = NewIdField()
    slug = SlugField()
    ingredient_groups = IngredientGroupSerializer(many=True)
    ingredients = IngredientUpdateSerializer(many=True)
    steps = StepUpdateSerializer(many=True)

    _errors: dict[str, Any]

    def save(self, **kwargs: Any) -> Recipe:
        """Save recipe and nested serializers."""
        # TODO: find a way to identify related fields
        related_fields: dict[str, RelatedSerializers] = {
            "ingredient_groups": IngredientGroupSerializer,
            "ingredients": IngredientUpdateSerializer,
            "steps": StepUpdateSerializer,
        }
        nested_serializer_data = {}
        for field_name in related_fields:
            nested_serializer_data[field_name] = self.validated_data.pop(field_name, [])

        recipe = super().save(**kwargs)

        for field_name, serializer_class in related_fields.items():
            self._save_nested(recipe, field_name, serializer_class, nested_serializer_data.get(field_name, []))

        return recipe

    def _save_nested(
        self,
        recipe: Recipe,
        field_name: str,
        serializer_class: type[IngredientGroupSerializer | StepUpdateSerializer | IngredientUpdateSerializer],
        data: list[dict[str, Any]],
    ) -> None:
        """Save nested data and handle errors."""
        existing_objects = {obj.pk: obj for obj in getattr(recipe, field_name).all()}
        new_objects_pks: list[int] = []
        errors: list[dict[str, Any]] = []
        deleted_pks: list[int] = []
        has_errors = False

        for item_data in data:
            item_pk = item_data.get("id", None)
            if item_pk and item_data.get("deleted", False):
                deleted_pks.append(item_pk)
                continue

            instance = existing_objects.get(item_pk)
            serializer = serializer_class(instance=instance, data=item_data, partial=True)
            if serializer.is_valid():
                obj = serializer.save(recipe=recipe)
                new_objects_pks.append(obj.pk)
                errors.append({})
            else:
                errors.append(serializer.errors)
                has_errors = True

        if has_errors:
            self._errors[field_name] = errors

        if deleted_pks:
            # Delete objects not in the new data
            getattr(recipe, field_name).filter(pk__in=deleted_pks).delete()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "cook_time",
            "prep_time",
            "yield_amount",
            "servings",
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
