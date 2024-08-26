from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Category, CategoryType

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest
    from django_stubs_ext import StrOrPromise


@admin.register(CategoryType)
class CategoryTypeAdmin(TranslationAdmin[CategoryType]):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("get_thumbnail", "name")
    ordering = ("name",)

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: CategoryType) -> StrOrPromise:
        """Add small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")


@admin.register(Category)
class CategoryAdmin(TranslationAdmin[Category]):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "type__name")
    list_display = ("get_thumbnail", "name", "type")
    ordering = ("name",)
    list_filter = ("type",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Category]:
        """Pre-select type for categories."""
        return super().get_queryset(request).select_related("type")

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: Category) -> StrOrPromise:
        """Add Small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")
