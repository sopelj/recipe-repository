from modeltranslation.translator import TranslationOptions, register

from .models import Food


@register(Food)
class FoodTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "aliases")
