from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Food

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


@admin.register(Food)
class FoodAdmin(TranslationAdmin):
    search_fields = ("name",)
    list_display = ("name", "get_used_count")
    ordering = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Food]:
        """Add count annotation in list mode."""
        if request.resolver_match.view_name == "admin:food_food_changelist":
            return Food.objects.annotate(used_count=Count("ingredients"))
        return Food.objects.all()

    @admin.display(description=_("Used count"), ordering="used_count")
    def get_used_count(self, obj: Food) -> str | None:
        """Display a count of how many times this food is used in various recipes."""
        return str(count) if (count := getattr(obj, "used_count", None)) else None
