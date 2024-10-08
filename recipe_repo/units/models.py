from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django.utils import translation
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from pint.errors import UndefinedUnitError

from ..common.models import NamedPluralModel
from ..common.utils import pluralize
from . import unit_registry
from .consts import System, UnitType
from .utils import format_fraction_amounts, format_imperial_amounts, format_metric_amounts

if TYPE_CHECKING:
    from decimal import Decimal

    import pint


logger = logging.getLogger(__name__)


class Unit(NamedPluralModel):
    name = models.CharField(_("Name"), max_length=150, unique=True)
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
    def unit(self) -> pint.Unit | None:
        """Return unit registry for this custom Unit."""
        if self.system:
            with translation.override("en"):
                try:
                    return unit_registry.Unit((self.abbreviation or self.name).lower())
                except UndefinedUnitError:
                    logger.warning("The unit %s was not defined in the unit registry", self.abbreviation)
        return None

    def format_amounts(self, amount: Decimal, max_amount: Decimal | None) -> tuple[str, Decimal]:
        """Format amounts based on this unit."""
        if self.unit and self.system == System.METRIC:
            return format_metric_amounts(amount, max_amount, self.unit)
        if self.unit and self.system == System.IMPERIAL:
            return format_imperial_amounts(amount, max_amount, self.unit)
        formatted_amount, count = format_fraction_amounts(amount, max_amount)
        return (
            gettext("{amount} {unit}").format(
                amount=formatted_amount,
                unit=pluralize(self.name, self.name_plural, count),
            ),
            count,
        )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ("-system", "type", "name")
