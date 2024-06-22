from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Custom User app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe_repo.users"
    label = "users"
    verbose_name = _("Users")
