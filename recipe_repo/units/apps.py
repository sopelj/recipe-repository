from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UnitsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe_repo.units"
    label = "units"
    verbose_name = _("Units")
