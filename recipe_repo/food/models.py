from __future__ import annotations

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..common.models import NamedPluralModel


class Food(NamedPluralModel):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    aliases = ArrayField(models.CharField(max_length=150), blank=True, default=list)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Food Item")
        verbose_name_plural = _("Food Items")
