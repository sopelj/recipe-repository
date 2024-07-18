from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Unit


@admin.register(Unit)
class UnitAdmin(TranslationAdmin):
    search_fields = ("name", "abbreviation")
    list_display = ("name", "name_plural", "abbreviation", "type", "system")
