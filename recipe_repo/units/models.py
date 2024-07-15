from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from ..common.models import NamedPluralModel


class System(TextChoices):
    METRIC = ("M", _("Metric"))
    IMPERIAL = ("I", _("Imperial"))


class UnitType(TextChoices):
    VOLUME = ("V", _("Volume"))
    WEIGHT = ("W", _("Weight"))
    OTHER = ("O", _("Other"))


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

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ("-system", "type", "name")
