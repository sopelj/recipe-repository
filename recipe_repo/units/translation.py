from modeltranslation.translator import TranslationOptions, register

from .models import Unit


@register(Unit)
class UnitTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "abbreviation")
