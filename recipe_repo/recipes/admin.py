from __future__ import annotations

from typing import TYPE_CHECKING, Any

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.shortcuts import redirect
from django.urls import URLPattern, path, resolve
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .forms import IngredientAdminForm, RecipeImportForm
from .models import (
    Category,
    Ingredient,
    IngredientGroup,
    IngredientQualifier,
    Recipe,
    Source,
    Step,
    UserRating,
    YieldUnit,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.db.models.fields.related import RelatedField
    from django.forms import ModelForm
    from django.http import HttpRequest, HttpResponseRedirect
    from django_stubs_ext import StrOrPromise


@admin.register(Category)
class CategoryAdmin(TranslationAdmin[Category]):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("get_thumbnail", "name", "top_level")
    ordering = ("name",)
    autocomplete_fields = ("parent_categories",)
    list_filter = ("parent_categories", "top_level")

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: Recipe) -> StrOrPromise:
        """Add Small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin[Source]):
    list_display = ("name", "type")
    search_fields = ("name", "value")
    list_filter = ("type",)


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin[UserRating]):
    list_display = ("get_user_full_name", "get_recipe_name", "rating")
    list_filter = [("user", admin.RelatedOnlyFieldListFilter), ("recipe", admin.RelatedOnlyFieldListFilter)]
    autocomplete_fields = ("user", "recipe")

    @admin.display(  # type: ignore[call-overload,misc]
        description=_("User"),
        ordering=("user__first_name", "user__last_name"),
    )
    def get_user_full_name(self, obj: UserRating) -> str:
        """Get full name of user for list view."""
        return obj.user.full_name or obj.user.email

    @admin.display(description=_("Recipe"), ordering=("recipe__name",))  # type: ignore[call-overload,misc]
    def get_recipe_name(self, obj: UserRating) -> str:
        """Get the name of a recipe for list view."""
        return obj.recipe.name

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserRating]:
        """Pre-fetch some fields in list mode."""
        if request.resolver_match and request.resolver_match.view_name == "admin:food_food_changelist":
            return UserRating.objects.select_related("user", "recipe")
        return UserRating.objects.filter()


@admin.register(YieldUnit)
class YieldUnitAdmin(TranslationAdmin[YieldUnit]):
    search_fields = ("name",)


@admin.register(IngredientQualifier)
class IngredientQualifierAdmin(TranslationAdmin[IngredientQualifier]):
    search_fields = ("title",)

    def save_model(
        self,
        request: HttpRequest,
        obj: IngredientQualifier,
        form: ModelForm[IngredientQualifier],
        change: bool,
    ) -> None:
        """Ensure lower case title for uniformity."""
        obj.title = obj.title.lower()
        super().save_model(request, obj, form, change)


class IngredientGroupInlineAdmin(
    SortableInlineAdminMixin,  # type: ignore[misc]
    TranslationTabularInline[IngredientGroup, Recipe],
):
    model = IngredientGroup
    extra = 0


class IngredientInlineAdmin(
    SortableInlineAdminMixin,  # type: ignore[misc]
    TranslationTabularInline[Ingredient, Recipe],
):
    model = Ingredient
    extra = 1
    form = IngredientAdminForm
    autocomplete_fields = ("food", "unit", "qualifier")
    fields = ("amount", "amount_max", "unit", "food", "qualifier", "optional", "note", "group")

    def get_field_queryset(
        self,
        db: Any,
        db_field: RelatedField[Any, Any],
        request: HttpRequest,
    ) -> QuerySet[Any, Any] | None:
        """Override queryset on ingredient groups to limit to those belonging to this recipe."""
        if db_field.name == "group":
            resolved = resolve(request.path_info)
            if recipe_id := resolved.kwargs.get("object_id"):
                return IngredientGroup.objects.filter(recipe_id=recipe_id)
            return IngredientGroup.objects.none()
        return super().get_field_queryset(db, db_field, request)


class StepInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline[Step, Recipe]):  # type: ignore[misc]
    model = Step
    extra = 1


class RecipeImportView(FormView[RecipeImportForm]):
    admin_site: admin.AdminSite
    template_name = "admin/recipe_import.html"
    form_class = RecipeImportForm

    def form_valid(self, form: RecipeImportForm) -> HttpResponseRedirect:
        """Check if recipe is imported successfully."""
        recipe = form.save()
        if not recipe.added_by_id and self.request.user.is_authenticated:
            recipe.added_by = self.request.user
            recipe.save()
        return redirect("admin:recipes_recipe_change", object_id=recipe.pk)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add form data to context."""
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        context.update(opts=Recipe._meta, **self.admin_site.each_context(self.request))  # noqa: SLF001
        return context


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, TranslationAdmin[Recipe]):  # type: ignore[misc]
    save_on_top = True
    search_fields = ("name",)
    readonly_fields = ("added_by",)
    list_display = ("get_thumbnail", "name", "get_categories")
    list_display_links = ("get_thumbnail", "name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("source", "categories", "parent_recipes", "added_by", "rated_by", "favourited_by")
    inlines = [IngredientGroupInlineAdmin, IngredientInlineAdmin, StepInlineAdmin]
    formfield_overrides = {
        models.DurationField: {"widget": TextInput(attrs={"placeholder": "HH:MM:SS"})},
    }

    def get_queryset(self, request: HttpRequest) -> QuerySet[Recipe]:
        """Avoid extra queries by pre-fetching categories."""
        return super().get_queryset(request).prefetch_related("categories")

    def get_urls(self) -> list[URLPattern]:
        """Add Import page to Recipe Admin URLs."""
        RecipeImportView.admin_site = self.admin_site
        view = self.admin_site.admin_view(RecipeImportView.as_view())  # type: ignore[type-var]
        return [path("import/", view, name="recipe_recipes_import"), *super().get_urls()]

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: Recipe) -> StrOrPromise:
        """Add Small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")

    @admin.display(description=_("Categories"))
    def get_categories(self, obj: Recipe) -> StrOrPromise:
        """Display categories as a coma-separated list."""
        return ", ".join(n for n in obj.categories.values_list("name", flat=True)) or _("No categories")

    def save_model(self, request: HttpRequest, obj: Recipe, form: ModelForm[Recipe], change: bool) -> None:
        """Automatically set added by to current user."""
        if not obj.added_by_id and request.user.is_authenticated:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
