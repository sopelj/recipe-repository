from modeltranslation.translator import TranslationOptions, register

from .models import Category, Ingredient, Preparation, Recipe, Step


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "slug")


@register(Preparation)
class PreparationTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Ingredient)
class IngredientTranslationOptions(TranslationOptions):
    fields = ("note",)


@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ("name", "slug")
