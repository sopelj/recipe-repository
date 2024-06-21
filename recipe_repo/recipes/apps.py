from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Recipes app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe_repo.recipes"
    app_name = "recipes"
