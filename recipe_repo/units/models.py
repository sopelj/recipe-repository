from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from ..common.models import NamedPluralModel
from . import unit_registry
from .consts import System, UnitType
from .utils import format_fraction_amounts, format_metric_amounts

if TYPE_CHECKING:
    from decimal import Decimal

    from pint import Unit as PintUnit


class Unit(NamedPluralModel):
    abbreviation = models.CharField(
        _("Abbreviation"),
        help_text=_("Abbreviation for unit. e.g tsp"),
        max_length=20,
        null=True,
        blank=True,
    )
    type = models.CharField(_("Type"), max_length=1, choices=UnitType.choices, default=UnitType.OTHER)
    system = models.CharField(_("System"), max_length=1, choices=System.choices, null=True, blank=True)

    @cached_property
    def unit(self) -> PintUnit | None:
        """Return unit registry for this custom Unit."""
        if self.system:
            with translation.override("en"):
                return unit_registry(self.abbreviation or self.name)
        return None

    def format_amounts(self, amount: Decimal, max_amount: Decimal | None) -> tuple[str, Decimal]:
        """Format amounts based on this unit."""
        if self.system == System.METRIC:
            return format_metric_amounts(amount, max_amount, self.unit)
        # TODO: Imperial
        return format_fraction_amounts(amount, max_amount)

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ("-system", "type", "name")
