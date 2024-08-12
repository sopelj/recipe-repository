from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InertiaConfig(AppConfig):
    """Recipes app config."""

    name = "recipe_repo.inertia"
    label = "inertia"
    verbose_name = _("Inertia")
