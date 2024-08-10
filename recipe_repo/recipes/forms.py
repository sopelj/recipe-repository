from __future__ import annotations

from decimal import Decimal
from urllib.parse import urlsplit, urlunsplit

import requests
from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from recipe_scrapers import AbstractScraper, WebsiteNotImplementedError, scrape_html

from .fields import FractionField
from .models import Ingredient, Recipe
from .recipe_importing import USER_AGENT, create_recipe_from_scraper


class ServingsForm(forms.Form):
    servings = forms.DecimalField(
        decimal_places=10,
        min_value=Decimal(0.125),
        max_value=Decimal(100),
        required=False,
        initial=Decimal(1),
    )


class IngredientAdminForm(forms.ModelForm[Ingredient]):
    """Custom form to allow for entering fractions into decimal fields for ease of use."""

    amount = FractionField(required=False)
    amount_max = FractionField(required=False)

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeImportForm(forms.ModelForm[Recipe]):
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
        recipe_html = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30).content
        try:
            self.scraper = scrape_html(recipe_html, org_url=url)
        except WebsiteNotImplementedError as e:
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
