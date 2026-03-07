from __future__ import annotations

import json
import logging
from functools import cached_property
from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError, transaction
from django.db.models import DecimalField, Prefetch, Q, Value
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from django.utils.translation import gettext
from django.views.generic.detail import SingleObjectMixin
from inertia import defer
from modeltranslation.utils import get_language
from recipe_scrapers._exceptions import FillPluginException, RecipeScrapersExceptions
from rest_framework.generics import get_object_or_404

from ..categories.models import Category
from ..categories.serializers import BaseCategorySerializer, CategorySerializer
from ..common.views import InertiaFormView, InertiaView
from ..food.models import Food
from ..units.models import Unit
from .forms import RecipeImportForm, RecipeReviewForm, ServingsForm
from .models import Ingredient, IngredientQualifier, Recipe
from .serializers import (
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
    RecipeUpdateSerializer,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


class RecipeListView(LoginRequiredMixin, InertiaView):
    component = "RecipeList"

    def get_component_props(self) -> dict[str, Any]:
        """Get all recipes or the recipes."""
        recipe_queryset = Recipe.objects.prefetch_related("categories", "categories__type").with_ratings()  # type: ignore[attr-defined]

        category, categories = None, None
        if category_slug := self.kwargs.get("category_slug"):
            category = get_object_or_404(Category.objects.select_related("type"), slug=category_slug)
            recipe_queryset = recipe_queryset.filter(categories__id__exact=category.pk)
        else:
            categories = Category.objects.select_related("type").filter(recipes__isnull=False).distinct()

        return {
            "recipes": RecipeListSerializer(recipe_queryset, many=True).data,
            "category": CategorySerializer(category).data if category else None,
            "categories": BaseCategorySerializer(categories, many=True).data if categories else None,
        }


def get_full_recipe(recipe_id: int) -> Recipe:
    """Ger the recipe with all necessary relationships."""
    recipe: Recipe = (
        Recipe.objects.select_related(
            "source",
            "nutrition",
            "yield_unit",
            "added_by",
        )
        .prefetch_related(
            Prefetch("categories", queryset=Category.objects.select_related("type").order_by("name")),
            "comments",
            "steps",
            "parent_recipes",
            "ingredient_groups",
        )
        .with_ratings()  # type: ignore[attr-defined]
        .get(pk=recipe_id)
    )
    return recipe


def get_recipe_ingredients(recipe_id: int, scale: float | bool = False) -> QuerySet[Ingredient]:
    """Get ingredients for a recipe."""
    ingredients =  Ingredient.objects.filter(recipe_id=recipe_id) \
            .select_related("unit", "food", "qualifier", "group")
    if scale is not False:
        ingredients = ingredients.annotate(scale=Value(scale or 1, output_field=DecimalField()))  # type: ignore[no-redef]
    return ingredients.order_by("group__order", "order")


class RecipeDetailView(InertiaFormView[RecipeReviewForm], SingleObjectMixin[Recipe]):
    component = "RecipeDetail"
    form_class = RecipeReviewForm

    def get_success_url(self) -> str:
        """Resolve detail view URL."""
        return reverse("recipes:recipe-detail", kwargs={"slug": self.kwargs.get("slug")})

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add extra params to form."""
        return super().get_form_kwargs() | {"user": self.request.user, "recipe_slug": self.kwargs.get("slug")}

    @cached_property
    def id_and_servings(self) -> tuple[int, int | None]:
        """Fetch PK and servings from Recipe and 404 if no match found."""
        try:
            slug = self.kwargs["slug"]
            return Recipe.objects.values_list("pk", "servings").get(
                Q(**{f"slug_{get_language()}": slug}) | Q(slug_en=slug),
            )
        except Recipe.DoesNotExist as e:
            raise Http404("Recipe does not exist.") from e

    def get_user_rating_favourite(self, recipe_id: int) -> tuple[int | None, bool]:
        """Get the user's rating and favourite state for the current recipe, if there is one."""
        if self.request.user.is_authenticated:
            try:
                rating = self.request.user.ratings.filter(recipe_id=recipe_id).values_list("rating", flat=True)[0]
            except IndexError:
                rating = None
            return rating, self.request.user.favourite_recipes.filter(id=recipe_id).exists()
        return None, False

    def get_component_props(self) -> dict[str, Any]:
        """Get props for RecipeDetail component."""
        recipe_id, servings = self.id_and_servings

        form = ServingsForm(self.request.GET, initial={"servings": servings})
        form.is_valid()
        scale = (form.cleaned_data.get("servings") or servings or 1) / (servings or 1)
        ingredients = get_recipe_ingredients(recipe_id, scale)
        user_rating, is_favourite = self.get_user_rating_favourite(recipe_id)
        return {
            "recipe": lambda: RecipeSerializer(get_full_recipe(recipe_id)).data,
            "servings": float((servings or 1) * scale),
            "ingredients": lambda: IngredientSerializer(ingredients, many=True).data,
            "userRating": user_rating,
            "userFavourite": is_favourite,
        }


class RecipeImportView(LoginRequiredMixin, InertiaFormView[RecipeImportForm]):
    """A user facing view for importing recipes."""

    form_class = RecipeImportForm
    object: Recipe

    def get_success_url(self) -> str:
        """Resolve detail view URL for newly created recipe."""
        if hasattr(self, "object"):
            return reverse("recipes:recipe-detail", kwargs={"slug": self.object.slug})
        return reverse("recipes:recipe-list")

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """Handle exceptions for import script."""
        form = self.get_form(self.get_form_class())
        if not form.is_valid():
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                recipe = form.save()
                recipe.added_by = self.request.user  # type: ignore[assignment]
                recipe.save()
                self.object = recipe
        except (DatabaseError, RecipeScrapersExceptions, FillPluginException):
            logger.exception("Failed to import recipe")
            self.request.session["errors"] = {"url": gettext("Error saving recipe")}
        return HttpResponseRedirect(self.get_success_url())


class RecipeEditView(LoginRequiredMixin, InertiaView):
    """A user facing view for importing recipes."""

    component = "RecipeEdit"
    object: Recipe | None = None

    def get_object(self, queryset: QuerySet[Recipe] | None = None) -> Recipe | None:
        """Return recipe object if on an update page or None otherwise."""
        if "slug" in self.kwargs and not self.object:
            recipe_slug = self.kwargs.get("slug")
            self.object = get_object_or_404(
                Recipe.objects.select_related("source").prefetch_related(
                    "steps",
                    "ingredient_groups",
                    "ingredients",
                ).filter(
                    Q(slug=recipe_slug) | Q(**{f"slug_{get_language()}": recipe_slug}),
                    added_by=self.request.user,  # type: ignore[misc]
                ),
            )
        return self.object

    def get_component_props(self) -> dict[str, Any]:
        """Get props for RecipeDetail component."""
        props = {
            "foods": defer(lambda: Food.objects.values("name", "id")),
            "units": defer(lambda: Unit.objects.values("name", "abbreviation", "id")),
            "qualifiers": defer(lambda: IngredientQualifier.objects.all().values("title", "id")),
        }
        if recipe := self.get_object():
            props |= {"recipe": lambda: RecipeUpdateSerializer(recipe).data}
        return props

    def get_success_url(self) -> str:
        """Resolve detail view URL for newly created recipe."""
        if obj := self.get_object():
            return reverse("recipes:recipe-edit", kwargs={"slug": obj.slug})
        return reverse("recipes:recipe-add")

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponseRedirect:
        """Handle special form cases for inertia."""
        serializer_kwargs = {"data": json.loads(self.request.body)}
        if obj := self.get_object():
            serializer_kwargs["instance"] = obj

        serializer = RecipeUpdateSerializer(**serializer_kwargs)
        if serializer.is_valid():
            self.object = serializer.save()
        else:
            self.request.session["errors"] = serializer.errors

        return HttpResponseRedirect(self.get_success_url())
