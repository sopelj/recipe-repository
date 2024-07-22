from rest_framework import serializers

from .models import Category, Ingredient, NutritionInformation, Recipe, Source, Step


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug")


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "name_plural", "slug", "thumbnail_image_url")


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionInformation
        exclude = ("recipe",)


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ("text", "order")


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("name", "type", "value")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("amount", "amount_max", "unit", "food", "optional")


class RecipeListSerializer(serializers.ModelSerializer):
    num_ratings = serializers.IntegerField()
    avg_ratings = serializers.IntegerField(allow_null=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ("name", "slug", "thumbnail_image_url", "description", "categories", "num_ratings", "avg_ratings")


class RecipeSerializer(RecipeListSerializer):
    steps = StepSerializer(many=True, read_only=True)
    source = SourceSerializer(read_only=True)
    nutrition = NutritionSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "name",
            "slug",
            "thumbnail_image_url",
            "description",
            "categories",
            "nutrition",
            "num_ratings",
            "avg_ratings",
            "ingredients",
            "steps",
            "source",
            "source_value",
            "servings",
            "yield_unit",
            "yield_amount",
        )
