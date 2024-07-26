from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from .consts import ureg
from ..common.models import NamedPluralModel

if TYPE_CHECKING:
    from pint import Unit as PintUnit


class System(TextChoices):
    METRIC = ("M", _("Metric"))
    IMPERIAL = ("I", _("Imperial"))


class UnitType(TextChoices):
    VOLUME = ("V", _("Volume"))
    WEIGHT = ("W", _("Weight"))
    OTHER = ("O", _("Other"))


def split_fractions(amount: Decimal):
    pass


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
        return ureg(self.name) if self.system else None

    def format_amount(self, amount: Decimal) -> tuple[Decimal, PintUnit]:
        if self.system == System.METRIC:
            out = (amount * self.unit).to_compact()
            return out.magnitude, out.unit
        if self.system == System.IMPERIAL:
            out = (amount * self.unit).to_compact()
        return

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ("-system", "type", "name")
