from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from recipe_scrapers import AbstractScraper, NoSchemaFoundInWildMode, WebsiteNotImplementedError, scrape_me

from .models import Recipe
from .recipe_importing import create_recipe_from_scraper


class RecipeImportForm(forms.ModelForm):
    """
    Take a URL and try and scrape it and build a recipe from it.

    This uses the library `recipe-scrapers`:
    https://github.com/hhursev/recipe-scrapers
    """

    scraper: AbstractScraper
    url = forms.URLField(
        label=_("Recipe URL"),
        help_text=_("Full URL to the desired recipe"),
        widget=forms.URLInput(attrs={"size": "100"}),
    )

    def clean(self) -> dict[str, str]:
        """Run scraping on form validation, so we can provide feedback."""
        url = urlunsplit((*urlsplit(self.cleaned_data["url"])[:3], None, None))
        try:
            self.scraper = scrape_me(url, wild_mode=True)
        except (WebsiteNotImplementedError, NoSchemaFoundInWildMode) as e:
            self.add_error("url", str(e))
        return self.cleaned_data

    def save(self, commit: bool = True) -> Recipe:
        """Actually try to parse the scraped recipe and return instance."""
        language = lang[:2] if (lang := self.scraper.language()) else settings.LANGUAGE_CODE
        with translation.override(language):
            recipe = create_recipe_from_scraper(self.scraper, self.cleaned_data["url"])
            if recipe is not None and commit is True:
                recipe.save()
            return recipe

    class Meta:
        model = Recipe
        fields = ("url",)
