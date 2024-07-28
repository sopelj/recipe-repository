from rest_framework import serializers

from .models import Category, Ingredient, NutritionInformation, Recipe, Source


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


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("name", "type", "value")


class IngredientSerializer(serializers.ModelSerializer):
    amount_display = serializers.SerializerMethodField()
    qualifier = serializers.SlugRelatedField(read_only=True, slug_field="title")
    group_id = serializers.IntegerField()

    def get_amount_display(self, obj: Ingredient) -> str:
        """Get formatted amount for display."""
        return obj.amount_display

    class Meta:
        model = Ingredient
        fields = ("id", "amount_display", "optional", "note", "qualifier", "group_id")


class RecipeListSerializer(serializers.ModelSerializer):
    num_ratings = serializers.IntegerField()
    avg_ratings = serializers.IntegerField(allow_null=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ("name", "slug", "thumbnail_image_url", "description", "categories", "num_ratings", "avg_ratings")


class RecipeSerializer(RecipeListSerializer):
    steps = serializers.SlugRelatedField(many=True, read_only=True, slug_field="text")
    source = SourceSerializer(read_only=True)
    nutrition = NutritionSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "name",
            "slug",
            "thumbnail_image_url",
            "description",
            "categories",
            "cook_time",
            "prep_time",
            "total_time",
            "nutrition",
            "num_ratings",
            "avg_ratings",
            "steps",
            "source",
            "source_value",
            "servings",
            "yield_unit",
            "yield_amount",
        )
