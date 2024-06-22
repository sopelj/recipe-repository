from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    """Categories for organizing recipes."""

    name = models.CharField(_("Name"), max_length=150, unique=True, help_text=_("Maximum 150 characters"))
    name_plural = models.CharField(max_length=150, null=True, blank=True)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Automatically generated from the name"))
    image = ThumbnailerImageField(_("Thumbnail"), upload_to="images/categories/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name_plural or self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)
