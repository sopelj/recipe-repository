from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from urllib.parse import urlsplit, urlunsplit

import requests
from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from recipe_scrapers import scrape_html
from recipe_scrapers._exceptions import RecipeScrapersExceptions

from .fields import FractionField
from .models import Ingredient, Recipe
from .recipe_importing import USER_AGENT, create_recipe_from_scraper

if TYPE_CHECKING:
    from .recipe_importing import Scraper


class ServingsForm(forms.Form):
    servings = forms.DecimalField(
        decimal_places=10,
        min_value=Decimal(0.125),
        max_value=Decimal(100),
        required=False,
        initial=Decimal(1),
    )


class RecipeReviewForm(forms.Form):
    favourite = forms.BooleanField(required=False)
    rating = forms.IntegerField(min_value=0, max_value=5, required=False)


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

    scraper: Scraper
    url = forms.URLField(
        label=_("Recipe URL"),
        help_text=_("Full URL to the desired recipe"),
        widget=forms.URLInput(attrs={"size": "100"}),
    )

    def clean(self) -> dict[str, str]:
        """Run scraping on form validation, so we can provide feedback."""
        url = urlunsplit((*urlsplit(self.cleaned_data["url"])[:3], None, None))
        recipe_html = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30).text
        try:
            self.scraper = scrape_html(recipe_html, org_url=url)  # type: ignore[assignment]
        except RecipeScrapersExceptions as e:
            self.add_error("url", str(e))
        return self.cleaned_data

    def save(self, commit: bool = True) -> Recipe:
        """Actually try to parse the scraped recipe and return instance."""
        language = lang[:2] if (lang := self.scraper.language()) else settings.LANGUAGE_CODE
        with translation.override(language):
            recipe = create_recipe_from_scraper(self.scraper, self.cleaned_data["url"])
            if recipe is None:
                raise forms.ValidationError(gettext("Failed to import recipe"))
            return recipe

    class Meta:
        model = Recipe
        fields = ("url",)
