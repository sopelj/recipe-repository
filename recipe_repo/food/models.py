from django.utils.translation import gettext_lazy as _

from ..common.models import NamedPluralModel


class Food(NamedPluralModel):
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Food")
