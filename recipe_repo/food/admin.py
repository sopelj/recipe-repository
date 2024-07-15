from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Food


@admin.register(Food)
class FoodAdmin(TranslationAdmin):
    pass
