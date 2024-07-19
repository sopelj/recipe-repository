from modeltranslation.translator import TranslationOptions, register

from .models import Category, Ingredient, IngredientQualifier, Recipe, Step, YieldUnit


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "slug")


@register(YieldUnit)
class YieldUnitTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural")


@register(IngredientQualifier)
class IngredientQualifierTranslationOptions(TranslationOptions):
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
