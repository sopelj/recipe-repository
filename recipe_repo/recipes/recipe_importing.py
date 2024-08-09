import contextlib
import logging
import re
import shutil
from datetime import timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError
from urllib.parse import urlsplit

import requests
from django.core.files import File
from django.db import IntegrityError
from django.db.models import Q
from recipe_scrapers import AbstractScraper
from slugify import slugify

from ..common.utils import to_snake_case
from ..food.models import Food
from ..units import unit_registry
from ..units.models import Unit
from ..units.utils import parse_numeric_string
from .models import (
    Category,
    Ingredient,
    IngredientGroup,
    IngredientQualifier,
    NutritionInformation,
    Recipe,
    Source,
    SourceTypes,
    Step,
    YieldUnit,
)

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1"
YIELD_REGEX = re.compile(r"^([0-9]+)\s?(.+)")
INGREDIENT_LINE_REGEX = re.compile(r"^([\u2150-\u215E\u00BC-\u00BE\d\s/-]+) (([\w.]*).+?)$")


def get_or_create_source(host: str, site_name: str | None) -> Source:
    """Get or create a Source based on hostname."""
    host = host.replace("www.", "")
    source = Source.objects.filter(
        Q(value__icontains=host) | Q(name__iexact=site_name or ""),
        type=SourceTypes.URL,
    ).first()
    if not source:
        return Source.objects.create(name=site_name or host, value=host, type=SourceTypes.URL)
    return source


def add_image_to_recipe(recipe: Recipe, image_url: str) -> None:
    """Download and save image from URL."""
    if not image_url.lower().startswith("http"):
        raise ValueError("Invalid image URL")
    with NamedTemporaryFile(delete=True) as temp_img:
        image_stream = requests.get(image_url, stream=True, headers={"User-Agent": USER_AGENT}, timeout=30)
        with contextlib.suppress(HTTPError):
            shutil.copyfileobj(image_stream.raw, temp_img)
            temp_img.flush()
            recipe.image.save(Path(image_url).name, File(temp_img))
            recipe.save()


def parse_yield_values(yields: str | None) -> tuple[int | None, str | None, int | None]:
    """Attempt to parse yields values from text."""
    yield_value, yield_unit, servings = None, None, None
    if yields and (match := YIELD_REGEX.match(yields)):
        value, unit = match.groups()
        with contextlib.suppress(ValueError):
            yield_value = int(value.strip())
        if unit and unit.lower().rstrip("s") == "serving":
            return None, None, yield_value
        if yield_value and unit and unit.lower() == "dozen":
            return None, None, yield_value * 12
        yield_unit = YieldUnit.objects.filter(
            Q(name__iexact=unit.rstrip("s")) | Q(name_plural__istartswith=unit),
        ).get_or_create(defaults={"name": unit.capitalize().rstrip("s"), "name_plural": unit.capitalize()})[0]
    return yield_value, yield_unit, servings


def extract_notes(text: str) -> tuple[str, str]:
    """Attempt to extract notes from ingredient line."""
    notes = ""
    remainder = text
    if matches := re.findall(r"(\(.+?\))", remainder, re.IGNORECASE):
        notes += " " + ", ".join(m.strip("() ") for m in matches)
        for match in matches:
            remainder = remainder.replace(match, "").strip()
    parts = remainder.split(",")
    if len(parts) > 1:
        remainder = parts[0]
        notes += " " + ", ".join(parts[1:])
    parts = re.split(r" (f?or) ", remainder, maxsplit=1)
    if len(parts) > 1:
        new_remainder = parts[0]
        notes += remainder.replace(new_remainder, "")
        remainder = new_remainder
    return remainder, notes.strip()


def parse_ingredient(recipe: Recipe, group: IngredientGroup, ingredient_text: str, order: int) -> None:
    """Attempt to parse the ingredient line into and Ingredient object."""
    if not (match := INGREDIENT_LINE_REGEX.match(ingredient_text.strip())):
        logger.warning("Unable to parse ingredient text. Might be title.")
        return

    # Amounts
    amount, remainder, unit = match.groups()
    if "-" in amount:
        amount, amount_max = amount.split("-", 1)
        amount_max = parse_numeric_string(amount_max)
    else:
        amount_max = None
    amount = parse_numeric_string(amount)

    # Units
    unit_clean = unit.rstrip(" s.")
    unit_instance = Unit.objects.filter(
        Q(name__iexact=unit_clean) | Q(name_plural__istartswith=unit_clean) | Q(abbreviation__iexact=unit_clean),
    ).first()
    if unit_instance:
        remainder = remainder.replace(unit, "").strip()  # remove unit

    # Check next word for qualifier. e.g. softened, cooked, chopped, etc.
    possible_qualifier = remainder.split(" ", maxsplit=1)[0]
    qualifier = IngredientQualifier.objects.filter(title__iexact=possible_qualifier).first()
    if qualifier:
        remainder = remainder.replace(possible_qualifier, "").strip()

    # Handle optional
    if match := re.search(r"\(?\s?optional(ly)?\s?\)?", remainder, re.IGNORECASE):
        remainder = remainder.replace(match.group(), "")
        optional = True
    else:
        optional = False

    # Extract notes and cleanup
    remainder, notes = extract_notes(remainder)
    remainder = " ".join([r for r in remainder.split(" ") if r]).strip(", ().")

    # Create food from remaining text
    food = Food.objects.filter(
        Q(name__iexact=remainder.rstrip("s")) | Q(name_plural__icontains=remainder),
    ).first()
    if not food:
        food = Food.objects.create(name=remainder.rstrip("s").capitalize())

    # Create ingredients
    Ingredient.objects.create(
        amount=amount,
        amount_max=amount_max,
        unit=unit_instance,
        food=food,
        group=group,
        optional=optional,
        recipe=recipe,
        note=notes or None,
        order=order,
    )


def get_nutrition_unit_value(name: str, value: str) -> float:
    """Get recommended unit based on value."""
    mg_values = ("potassiumContent", "sodiumContent", "cholesterolContent")
    unit = "mg" if name in mg_values else "g"
    return unit_registry(value).to(unit).magnitude


def create_nutrition_information(recipe: Recipe, nutrition: dict[str, str]) -> None:
    """Create Nutrition information from schema data."""
    NutritionInformation.objects.create(
        recipe=recipe,
        calories=(
            parse_numeric_string(calories.split(" ")[0]) if (calories := nutrition.pop("calories", None)) else None
        ),
        serving_size=(
            parse_numeric_string(servings.split(" ")[0]) if (servings := nutrition.pop("servingSize", None)) else 1
        ),
        **{
            to_snake_case(name.replace("Content", "")): get_nutrition_unit_value(name, value)
            for name, value in nutrition.items()
            if value
        },
    )


def create_recipe_from_scraper(scraper: AbstractScraper, url: str) -> Recipe | None:
    """Take a scraper and try to create a recipe from it."""
    title = scraper.title()
    host = scraper.host() or urlsplit(url).hostname
    recipe = Recipe(
        name=title,
        slug=slugify(title),
        source_value=url,
        cook_time=timedelta(minutes=cook_time) if (cook_time := scraper.cook_time()) else None,
        prep_time=timedelta(minutes=pre_time) if (pre_time := scraper.prep_time()) else None,
        source=get_or_create_source(host, scraper.site_name()),
        description=scraper.description(),
    )
    try:
        recipe.save()
    except IntegrityError:
        return None

    if image_url := scraper.image():
        add_image_to_recipe(recipe, image_url)

    recipe.yield_label, recipe.yield_unit, recipe.servings = parse_yield_values(scraper.yields())
    recipe.save()

    # Create one Step for each line in recipe instructions
    Step.objects.bulk_create(
        [
            Step(text=instruction.strip(), recipe=recipe, order=i + 1)
            for i, instruction in enumerate(scraper.instructions_list())
            if instruction.strip()
        ],
    )

    # Parse all ingredients
    ingredient_order = 0
    for group in scraper.ingredient_groups():
        ingredient_group = None
        if group.purpose:
            ingredient_group = IngredientGroup.objects.create(recipe=recipe, text=group.purpose, order=ingredient_order)
            ingredient_order += 1
        for ingredient_line in group.ingredients:
            parse_ingredient(recipe, ingredient_group, ingredient_line, ingredient_order)
            ingredient_order += 1

    if nutrients := scraper.nutrients():
        create_nutrition_information(recipe, nutrients)

    # Try and match to existing categories
    if categories := (scraper.category() or "").split(","):
        filters = Q()
        for category_name in categories:
            filters |= Q(name__iexact=category_name)
        if matching_categories := Category.objects.filter(filters).values_list("pk", flat=True):
            recipe.categories.set(matching_categories)

    recipe.save()
    return recipe
