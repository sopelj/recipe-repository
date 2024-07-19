import operator
import re
from datetime import timedelta
from functools import reduce

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from treebeard.mp_tree import MP_Node

from ..common.models import NamedModel, NamedPluralModel

RATING_CHOICES = (
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


class Category(MP_Node, NamedPluralModel):
    """Categories for organizing recipes."""

    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Thumbnail"), upload_to="images/categories/", null=True, blank=True)

    @property
    def thumbnail_image_url(self) -> str | None:
        """Resolve URL of the user's profile image."""
        return get_thumbnailer(self.image)["thumbnail"].url if self.image else None

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)


class UserRating(models.Model):
    rating = models.PositiveIntegerField(_("Rating"), choices=RATING_CHOICES, null=True, blank=True)
    recipe = models.ForeignKey("Recipe", related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", related_name="ratings", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("User Rating")
        verbose_name_plural = _("User Ratings")


class YieldUnit(NamedPluralModel):
    class Meta:
        verbose_name = _("Yield Unit")
        verbose_name_plural = _("Yield Units")


class SourceTypes(models.IntegerChoices):
    URL = 1, _("URL")
    BOOK = 2, _("Book")
    PERSON = 3, _("Person")
    OTHER = 4, _("Other")


class Source(NamedModel):
    type = models.PositiveIntegerField(_("Type"), choices=SourceTypes.choices, default=SourceTypes.URL)
    value = models.CharField(_("Value"), blank=True, null=True, max_length=200)

    @staticmethod
    def validate_value(value: int | str, source_type: SourceTypes) -> None:
        """Validate values if types if URL or Book."""
        if source_type == SourceTypes.URL:
            URLValidator()(value)
        elif (
            source_type == SourceTypes.BOOK
            and value is not None
            and not re.match(r"(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)", value)
        ):
            raise ValidationError("Invalid ISBN value")

    def get_value_display(self) -> str:
        """Format certain types of sources with useful links instead of static values."""
        if self.type == SourceTypes.URL.value:
            return mark_safe(f'<a href="{self.value}">{self.name}</a>')  # noqa: S308
        if self.type == SourceTypes.BOOK.value:
            return mark_safe(f'<a href="https://isbnsearch.org/search?s={self.value}">{self.name}</a>')  # noqa: S308
        return f"{self.name}: {self.value}" if self.value else self.name

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")


class Recipe(NamedModel):
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Image"), upload_to="images/recipes/", null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    prep_time = models.DurationField(_("Prep time"), blank=True, null=True)
    cook_time = models.DurationField(_("Cook time"), blank=True, null=True)
    cook_time_max = models.DurationField(_("Max cook time"), blank=True, null=True)
    servings = models.PositiveIntegerField(_("Servings"), null=True, blank=True)
    yield_amount = models.PositiveIntegerField(_("Yield"), null=True, blank=True)
    yield_unit = models.ForeignKey(YieldUnit, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, verbose_name=_("Source"), blank=True, null=True, on_delete=models.SET_NULL)
    source_value = models.CharField(_("Source Value"), blank=True, null=True, max_length=250)

    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), blank=True, related_name="recipes")
    parent_recipes = models.ManyToManyField(
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
    rated_by = models.ManyToManyField(
        "users.User",
        related_name="rated_recipes",
        blank=True,
        through=UserRating,
        verbose_name=_("Rated by"),
    )

    @property
    def total_time(self) -> timedelta:
        """Return total time combining prep and cook times."""
        times = [t for t in [self.prep_time, (self.cook_time_max or self.cook_time)] if t]
        return reduce(operator.add, times) if times else timedelta()

    @property
    def thumbnail_image_url(self) -> str | None:
        """Resolve URL of recipe thumbnail image."""
        return get_thumbnailer(self.image)["thumbnail"].url if self.image else None

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("name",)


class IngredientQualifier(models.Model):
    title = models.CharField(_("Title"), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Ingredient Qualifier")
        verbose_name_plural = _("Ingredient Qualifiers")


class Ingredient(models.Model):
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), null=True, blank=True, max_digits=10, decimal_places=4)
    amount_max = models.DecimalField(_("Max Amount"), null=True, blank=True, max_digits=10, decimal_places=4)
    note = models.CharField(_("Note"), max_length=100, blank=True)
    optional = models.BooleanField(_("Optional"), default=False)

    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), on_delete=models.CASCADE, related_name="ingredients")
    unit = models.ForeignKey("units.Unit", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    food = models.ForeignKey("food.Food", verbose_name=_("Food"), on_delete=models.CASCADE, related_name="+")
    qualifier = models.ForeignKey(
        IngredientQualifier,
        verbose_name=_("Qualifier"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")
        ordering = ("order",)


class Step(models.Model):
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), related_name="steps", on_delete=models.CASCADE)
    text = models.TextField(_("Text"), blank=True)

    def __str__(self) -> str:
        """Display truncated text as string value."""
        return f"{self.text[:25]}..." if len(self.text) > 25 else self.text

    class Meta:
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")
        ordering = ("order",)
