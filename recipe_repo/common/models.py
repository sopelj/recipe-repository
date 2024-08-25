from __future__ import annotations

from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _


class NamedModel(models.Model):
    name = models.CharField(_("Name"), max_length=150)

    @override
    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class NamedPluralModel(NamedModel):
    name_plural = models.CharField(_("Plural Name"), max_length=150, null=True, blank=True)

    @override
    def __str__(self) -> str:
        return self.name_plural or self.name

    class Meta:
        abstract = True
