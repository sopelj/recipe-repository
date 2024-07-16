from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from treebeard.mp_tree import MP_Node

from ..common.models import NamedPluralModel


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
