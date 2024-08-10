from __future__ import annotations

from django.utils.translation import gettext_lazy as _

from ..common.models import NamedPluralModel


class Food(NamedPluralModel):

    class Meta:
        ordering = ("name",)
        verbose_name = _("Food Item")
        verbose_name_plural = _("Food Items")
