from __future__ import annotations

import re
from functools import cached_property
from typing import TYPE_CHECKING, Never, override

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models.aggregates import Avg, Count
from django.utils.html import format_html
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from modeltranslation.manager import MultilingualQuerySet

from ..common.models import NamedModel, NamedPluralModel
from ..common.utils import pluralize
from ..units.consts import UnitType
from ..units.utils import format_fraction_amounts

if TYPE_CHECKING:
    from datetime import timedelta
    from decimal import Decimal
    from typing import TypedDict

    from django.db.models import ManyToManyField
    from django_stubs_ext import StrOrPromise, WithAnnotations
    from django_stubs_ext.db.models.manager import RelatedManager

    class RecipeRatings(TypedDict):
        avg_rating: float
        num_ratings: int | None


class YieldUnit(NamedPluralModel):
    recipe_set: RelatedManager[Recipe]

    name = models.CharField(_("Name"), max_length=150, unique=True)

    class Meta:
        verbose_name = _("Yield Unit")
        verbose_name_plural = _("Yield Units")


class SourceTypes(models.IntegerChoices):
    URL = 1, _("URL")
    BOOK = 2, _("Book")
    PERSON = 3, _("Person")
    OTHER = 4, _("Other")


class Source(NamedModel):
    recipe_set: RelatedManager[Recipe]

    name = models.CharField(_("Name"), max_length=150, unique=True)
    type = models.PositiveIntegerField(_("Type"), choices=SourceTypes.choices, default=SourceTypes.URL)
    value = models.CharField(_("Value"), blank=True, null=True, max_length=200)

    @staticmethod
    def validate_value(value: str, source_type: SourceTypes) -> None:
        """Validate values if types if URL or Book."""
        if source_type == SourceTypes.URL:
            URLValidator()(value)
        elif source_type == SourceTypes.BOOK and value and not re.match(r"(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)", value):
            raise ValidationError("Invalid ISBN value")

    def get_value_display(self) -> str:
        """Format certain types of sources with useful links instead of static values."""
        if self.type == SourceTypes.URL.value:
            return format_html('<a href="{}">{}</a>', self.value, self.name)
        if self.type == SourceTypes.BOOK.value:
            return format_html('<a href="https://isbnsearch.org/search?s={}">{}</a>', self.value, self.name)
        return f"{self.name}: {self.value}" if self.value else self.name

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")


class RecipeQuerySet(MultilingualQuerySet["Recipe"]):
    def with_ratings(self) -> RecipeQuerySet[WithAnnotations[Recipe, RecipeRatings]]:  # type: ignore[type-arg]
        """Return Queryset with rating annotations."""
        return self.annotate(
            avg_rating=Avg("ratings__rating"),
            num_ratings=Count("ratings"),
        )


class Recipe(NamedModel):
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Image"), upload_to="images/recipes/", null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    prep_time = models.DurationField(_("Prep time"), blank=True, null=True)
    cook_time = models.DurationField(_("Cook time"), blank=True, null=True)
    cook_time_max = models.DurationField(_("Max cook time"), blank=True, null=True)
    servings = models.PositiveIntegerField(_("Servings"), null=True, blank=True)
    yield_amount = models.PositiveIntegerField(_("Yield"), null=True, blank=True)
    yield_unit = models.ForeignKey(YieldUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    source = models.ForeignKey(
        Source,
        verbose_name=_("Source"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    source_value = models.CharField(_("Source Value"), blank=True, null=True, max_length=250)

    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name=_("Categories"),
        blank=True,
        related_name="recipes",
    )
    parent_recipes: ManyToManyField[Recipe, Never] = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="sub_recipes",
        verbose_name=_("Parent recipes"),
    )
    added_by = models.ForeignKey(
        "users.User",
        related_name="my_recipes",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Added by"),
    )

    objects: models.Manager[Recipe] = RecipeQuerySet.as_manager()

    @property
    def total_time(self) -> timedelta | None:
        """Return total time combining prep and cook times."""
        if self.prep_time and self.cook_time:
            return self.prep_time + self.cook_time
        return self.prep_time or self.cook_time

    @property
    def thumbnail_url(self) -> str | None:
        """Resolve URL of recipe thumbnail image."""
        return get_thumbnailer(self.image)["thumbnail"].url if self.image else None

    @property
    def image_url(self) -> str | None:
        """Resolve URL of recipe thumbnail image."""
        return get_thumbnailer(self.image)["image"].url if self.image else None

    def get_absolute_url(self) -> str:
        """Resolve recipe URL in current language."""
        return gettext("/en/recipes/{slug}/").format(slug=self.slug)

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("name",)


class IngredientQualifier(models.Model):
    title = models.CharField(_("Title"), max_length=100, unique=True)

    @override
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Ingredient Qualifier")
        verbose_name_plural = _("Ingredient Qualifiers")


class IngredientGroup(NamedModel):
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("Recipe"),
        on_delete=models.CASCADE,
        related_name="ingredient_groups",
    )

    class Meta:
        ordering = ("order",)
        unique_together = ("name", "recipe")
        verbose_name = _("Ingredient Group")
        verbose_name_plural = _("Ingredient Groups")


class NutritionInformation(models.Model):
    calories = models.PositiveIntegerField(_("Calories"), help_text=_("in kilo-calories"))
    serving_size = models.PositiveIntegerField(_("Serving Size"), help_text=_("number of servings this corresponds to"))
    fat = models.PositiveIntegerField(_("Fat"), help_text=_("in grams"), null=True, blank=True)
    saturated_fat = models.PositiveIntegerField(_("Saturated Fat"), help_text=_("in grams"), null=True, blank=True)
    trans_fat = models.PositiveIntegerField(_("Trans Fat"), help_text=_("in grams"), null=True, blank=True)
    unsaturated_fat = models.PositiveIntegerField(_("Unsaturated Fat"), help_text=_("in grams"), null=True, blank=True)
    cholesterol = models.PositiveIntegerField(_("Cholesterol"), help_text=_("in milligrams"), null=True, blank=True)
    sodium = models.PositiveIntegerField(_("Sodium"), help_text=_("in milligrams"), null=True, blank=True)
    potassium = models.PositiveIntegerField(_("Potassium"), help_text=_("in milligrams"), null=True, blank=True)
    carbohydrate = models.PositiveIntegerField(_("Carbohydrates"), help_text=_("in grams"), null=True, blank=True)
    fiber = models.PositiveIntegerField(_("Fiber"), help_text=_("in grams"), null=True, blank=True)
    sugar = models.PositiveIntegerField(_("Sugar"), help_text=_("in grams"), null=True, blank=True)
    protein = models.PositiveIntegerField(_("Protein"), help_text=_("in grams"), null=True, blank=True)
    recipe = models.OneToOneField(Recipe, related_name="nutrition", verbose_name=_("Recipe"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Nutritional Information")
        verbose_name_plural = _("Nutritional Information")


class Ingredient(models.Model):
    # Scale that can be overwritten
    scale: int = 1

    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), null=True, blank=True, max_digits=10, decimal_places=5)
    amount_max = models.DecimalField(_("Max Amount"), null=True, blank=True, max_digits=10, decimal_places=5)
    note = models.CharField(_("Note"), max_length=100, blank=True)
    optional = models.BooleanField(_("Optional"), default=False)

    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), on_delete=models.CASCADE, related_name="ingredients")
    unit = models.ForeignKey("units.Unit", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    food = models.ForeignKey("food.Food", verbose_name=_("Food"), on_delete=models.CASCADE, related_name="ingredients")
    qualifier = models.ForeignKey(
        IngredientQualifier,
        verbose_name=_("Qualifier"),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    group = models.ForeignKey(
        IngredientGroup,
        verbose_name=_("Group"),
        null=True,
        blank=True,
        related_name="ingredients",
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return f"{self.amount_display} {self.food_display}"

    @cached_property
    def scaled_amount(self) -> Decimal | None:
        """Amount scaled."""
        return self.amount * self.scale if self.amount else None

    @cached_property
    def scaled_amount_max(self) -> Decimal | None:
        """Max amount scaled."""
        return (self.amount_max * self.scale) if self.amount_max else None

    @cached_property
    def formatted_amounts(self) -> tuple[str, Decimal | None]:
        """Return the formatted amount and the count for pluralising."""
        if not self.scaled_amount:
            return "", None
        if self.unit:
            return self.unit.format_amounts(self.scaled_amount, self.scaled_amount_max)
        return format_fraction_amounts(self.scaled_amount, self.scaled_amount_max)

    @cached_property
    def amount_display(self) -> str:
        """Nicely format amount(s) and food for display."""
        return self.formatted_amounts[0]

    @cached_property
    def food_display(self) -> StrOrPromise:
        """Return Food pluralised based on formatted amounts."""
        if self.unit and self.unit.type != UnitType.OTHER:
            # When dealing with weight or volume based units always use the plural name if defined
            # One may say "1 almond", but it would be "1 cup almonds" regardless of number.
            return self.food.name_plural or self.food.name
        return pluralize(self.food.name, self.food.name_plural, self.formatted_amounts[1] or 0)

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")
        ordering = ("order",)


class Step(models.Model):
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), related_name="steps", on_delete=models.CASCADE)
    text = models.TextField(_("Text"), blank=True)

    @override
    def __str__(self) -> str:
        """Display truncated text as string value."""
        return f"{self.text[:25]}..." if len(self.text) > 25 else self.text

    class Meta:
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")
        ordering = ("order",)
