from __future__ import annotations

from typing import TYPE_CHECKING, Any

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import URLPattern, path
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
    from django.forms import ModelForm
    from django.http import HttpRequest, HttpResponseRedirect


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("get_thumbnail", "name", "top_level")
    ordering = ("name",)
    autocomplete_fields = ("parent_categories",)
    list_filter = ("parent_categories", "top_level")

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: Recipe) -> str:
        """Add Small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("value",)
    search_fields = ("name", "value")


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ("get_user_full_name", "get_recipe_name", "rating")
    list_filter = [("user", admin.RelatedOnlyFieldListFilter), ("recipe", admin.RelatedOnlyFieldListFilter)]
    autocomplete_fields = ("user", "recipe")

    @admin.display(description=_("User"), ordering=("user__first_name", "user__last_name"))
    def get_user_full_name(self, obj: UserRating) -> str:
        """Get full name of user for list view."""
        return obj.user.full_name or obj.user.email

    @admin.display(description=_("Recipe"), ordering=("recipe__name",))
    def get_recipe_name(self, obj: UserRating) -> str:
        """Get the name of a recipe for list view."""
        return obj.recipe.name

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserRating]:
        """Pre-fetch some fields in list mode."""
        if request.resolver_match.view_name == "admin:food_food_changelist":
            return UserRating.objects.select_related("user", "recipe")
        return UserRating.objects.filter()


@admin.register(YieldUnit)
class YieldUnitAdmin(TranslationAdmin):
    search_fields = ("name",)


@admin.register(IngredientQualifier)
class IngredientQualifierAdmin(TranslationAdmin):
    search_fields = ("title",)

    def save_model(self, request: HttpRequest, obj: IngredientQualifier, form: ModelForm, change: bool) -> None:
        """Ensure lower case title for uniformity."""
        obj.title = obj.title.lower()
        super().save_model(request, obj, form, change)


class IngredientGroupInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = IngredientGroup
    extra = 0


class IngredientInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = Ingredient
    extra = 1
    form = IngredientAdminForm
    autocomplete_fields = ("food", "unit", "qualifier")
    fields = ("amount", "amount_max", "unit", "food", "qualifier", "optional", "note", "group")


class StepInlineAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = Step
    extra = 1


class RecipeImportView(FormView):
    admin_site: admin.AdminSite
    template_name = "admin/recipe_import.html"
    form_class = RecipeImportForm

    def form_valid(self, form: RecipeImportForm) -> HttpResponseRedirect:
        """Check if recipe is imported successfully."""
        recipe = form.save()
        if recipe is None:
            form.add_error("url", _("Failed to create a recipe from the provided URL"))
            return self.form_invalid(form)
        if not recipe.added_by_id:
            recipe.added_by = self.request.user
            recipe.save()
        return redirect("admin:recipes_recipe_change", object_id=recipe.pk)

    def get_context_data(self, **kwargs: Any):
        """Add form data to context."""
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        context.update(opts=Recipe._meta, **self.admin_site.each_context(self.request))  # noqa: SLF001
        return context


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, TranslationAdmin):
    save_on_top = True
    search_fields = ("name",)
    list_display = ("get_thumbnail", "name", "get_categories")
    list_display_links = ("get_thumbnail", "name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("source", "categories", "parent_recipes", "added_by", "rated_by", "favourited_by")
    inlines = [IngredientGroupInlineAdmin, IngredientInlineAdmin, StepInlineAdmin]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Recipe]:
        """Avoid extra queries by pre-fetching categories."""
        return super().get_queryset(request).prefetch_related("categories")

    def get_urls(self) -> list[URLPattern]:
        """Add Import page to Recipe Admin URLs."""
        RecipeImportView.admin_site = self.admin_site
        view = self.admin_site.admin_view(RecipeImportView.as_view())
        return [path("import/", view, name="recipe_recipes_import"), *super().get_urls()]

    @admin.display(description=_("Thumbnail"))
    def get_thumbnail(self, obj: Recipe) -> str:
        """Add Small thumbnail to recipe admin list view."""
        if obj.image:
            return format_html('<img src="{}" />', obj.image["admin"].url)
        return _("No thumbnail")

    @admin.display(description=_("Categories"))
    def get_categories(self, obj: Recipe) -> str:
        """Display categories as a coma-separated list."""
        return ", ".join(n for n in obj.categories.values_list("name", flat=True)) or _("No categories")

    def save_model(self, request: HttpRequest, obj: Recipe, form: ModelForm, change: bool) -> None:
        """Automatically set added by to current user."""
        if not obj.added_by_id:
            obj.added_by_id = request.user
        super().save_model(request, obj, form, change)
