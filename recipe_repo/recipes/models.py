import operator
from datetime import timedelta
from functools import reduce

from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from treebeard.mp_tree import MP_Node

from ..common.models import NamedModel, NamedPluralModel


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


class Recipe(NamedModel):
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Image"), upload_to="images/recipes/", null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    prep_time = models.DurationField(_("Prep time"), blank=True, null=True)
    cook_time = models.DurationField(_("Cook time"), blank=True, null=True)
    cook_time_max = models.DurationField(_("Max cook time"), blank=True, null=True)
    servings = models.PositiveIntegerField(_("Servings"), null=True, blank=True)

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


class Preparation(models.Model):
    title = models.CharField(_("Title"), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Preparation")
        verbose_name_plural = _("Preparations")


class Ingredient(models.Model):
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), null=True, blank=True, max_digits=10, decimal_places=4)
    amount_max = models.DecimalField(_("Max Amount"), null=True, blank=True, max_digits=10, decimal_places=4)
    note = models.CharField(_("Note"), max_length=100, blank=True)
    optional = models.BooleanField(_("Optional"), default=False)

    recipe = models.ForeignKey(Recipe, verbose_name=_("Recipe"), on_delete=models.CASCADE, related_name="ingredients")
    unit = models.ForeignKey("units.Unit", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    food = models.ForeignKey("food.Food", verbose_name=_("Food"), on_delete=models.CASCADE, related_name="+")
    prep = models.ForeignKey(
        Preparation,
        verbose_name=_("Prep"),
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
