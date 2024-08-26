from modeltranslation.translator import TranslationOptions, register

from .models import Category, CategoryType


@register(CategoryType)
class CategoryTypeTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "slug")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "name_plural", "slug")
