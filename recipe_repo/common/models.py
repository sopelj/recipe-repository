from django.db import models
from django.utils.translation import gettext_lazy as _


class NamedModel(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class NamedPluralModel(NamedModel):
    name_plural = models.CharField(_("Plural Name"), max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name_plural or self.name

    class Meta:
        abstract = True
