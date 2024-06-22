from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipesConfig(AppConfig):
    """Recipes app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe_repo.recipes"
    label = "recipes"
    verbose_name = _("Recipes")
