from __future__ import annotations

from typing import TYPE_CHECKING

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationBaseModelAdmin, TranslationTabularInline
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category, Ingredient, Preparation, Recipe, Step

if TYPE_CHECKING:
    from django.forms import ModelForm
    from django.http import HttpRequest


@admin.register(Category)
class CategoryAdmin(TreeAdmin, TranslationBaseModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    form = movenodeform_factory(Category, exclude=("name", "name_plural", "slug"))


@admin.register(Preparation)
class PreparationAdmin(TranslationAdmin):
    search_fields = ("title",)

    def save_model(self, request: HttpRequest, obj: Preparation, form: ModelForm, change: bool) -> None:
        """Ensure lower case title for uniformity."""
        obj.title = obj.title.lower()
        super().save_model(request, obj, form, change)


class IngredientInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = Ingredient
    extra = 1
    autocomplete_fields = ("food", "unit", "prep")
    fields = ("amount", "amount_max", "unit", "food", "prep", "optional", "note")


class StepInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = Step
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, TranslationAdmin):
    save_on_top = True
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("categories", "parent_recipes", "added_by")
    inlines = [IngredientInlineAdmin, StepInlineAdmin]

    def save_model(self, request: HttpRequest, obj: Recipe, form: ModelForm, change: bool) -> None:
        """Automatically set added by to current user."""
        if not obj.added_by_id:
            obj.added_by_id = request.user
        super().save_model(request, obj, form, change)
