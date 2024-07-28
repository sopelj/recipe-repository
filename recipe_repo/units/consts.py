from __future__ import annotations

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class System(TextChoices):
    METRIC = ("M", _("Metric"))
    IMPERIAL = ("I", _("Imperial"))


class UnitType(TextChoices):
    VOLUME = ("V", _("Volume"))
    WEIGHT = ("W", _("Weight"))
    OTHER = ("O", _("Other"))
