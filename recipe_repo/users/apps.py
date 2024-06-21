from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Custom User app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe_repo.users"
    app_name = "users"
