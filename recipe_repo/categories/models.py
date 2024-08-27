from __future__ import annotations

from functools import cached_property
from typing import override

from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

from recipe_repo.common.models import NamedPluralModel


class BaseCategory(NamedPluralModel):
    """Categories for organizing recipes."""

    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Thumbnail"), upload_to="images/categories/", null=True, blank=True)

    @property
    def thumbnail_url(self) -> str | None:
        """Resolve URL of the user's profile image."""
        return get_thumbnailer(self.image)["thumbnail"].url if self.image else None

    class Meta:
        abstract = True
        ordering = ("name",)


class CategoryType(BaseCategory):
    class Meta:
        ordering = ("name",)
        verbose_name = _("Category Type")
        verbose_name_plural = _("Category types")


class Category(BaseCategory):
    type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name="categories")

    @cached_property
    def tag(self) -> str:
        """Return a tag label including type."""
        return gettext("{tag}: {category}").format(tag=self.type.name, category=self.name)

    @override
    def __str__(self) -> str:
        return self.tag

    class Meta:
        ordering = ("name",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
