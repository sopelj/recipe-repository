import contextlib
import logging
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from tempfile import NamedTemporaryFile
from unicodedata import numeric
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from django.core.files import File
from django.db import IntegrityError
from django.db.models import Q
from recipe_scrapers import AbstractScraper
from slugify import slugify

from ..food.models import Food
from ..units.models import Unit
from .models import Ingredient, Recipe, Source, SourceTypes, Step, YieldUnit

logger = logging.getLogger(__name__)


def get_or_create_source(host: str) -> Source:
    """Get or create a Source based on hostname."""
    return Source.objects.get_or_create(
        value__icontains=host.replace("www.", ""),
        type=SourceTypes.URL,
        defaults={"name": host.capitalize(), "value": f"https://{host}"},
    )[0]


def add_image_to_recipe(recipe: Recipe, image_url: str) -> None:
    """Download and save image from URL."""
    if not image_url.lower().startswith("http"):
        raise ValueError("Invalid image URL")
    with NamedTemporaryFile(delete=True) as img_temp:
        image_request = Request(image_url, headers={"User-Agent": "Magic Browser"})  # noqa: S310
        with contextlib.suppress(HTTPError):
            img_temp.write(urlopen(image_request).read())  # noqa: S310
            img_temp.flush()
            recipe.image.save(Path(image_url).name, File(img_temp))
            recipe.save()


def parse_yield_values(yields: str | None) -> tuple[int | None, str | None, int | None]:
    """Attempt to parse yields values from text."""
    yield_value, yield_unit, servings = None, None, None
    if yields and (match := re.match(r"^([0-9]+)(.+)", yields)):
        value, unit = match.groups()
        with contextlib.suppress(ValueError):
            yield_value = int(value.strip())
        if yield_unit == "servings":
            return None, None, yield_value
        yield_unit = YieldUnit.objects.filter(
            Q(name__iexact=unit.rstrip("s")) | Q(name_plural__istartswith=unit),
        ).get_or_create(defaults={"name": unit.capitalize().rstrip("s"), "name_plural": unit.capitalize()})[0]
    return yield_value, yield_unit, servings


def parse_numeric_string(value: str) -> Decimal:
    """Attempt to parse a string that could be an int or fraction into a decimal."""
    match = re.match(r"(([0-9]*\s?)?(([0-9]+/[0-9]+)|([\u2150-\u215E\u00BC-\u00BE])))|([0-9]+)", value.strip(" "))
    whole, __, fraction, fake_fraction, only_num = match.groups()[1:]
    amount = int(num) if (num := only_num or whole) else 0
    if fraction and (f := Fraction(fraction)):
        amount += f.numerator / f.denominator
    elif fake_fraction:
        amount += numeric(fake_fraction)
    return Decimal(amount)


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
        return new_remainder, notes + remainder.replace(new_remainder, "")
    return remainder, notes


def parse_ingredient(recipe: Recipe, ingredient_text: str, order: int) -> None:
    """Attempt to parse the ingredient line into and Ingredient object."""
    if not (match := re.match(r"^([\u2150-\u215E\u00BC-\u00BE\d\s/-]+) (([\w.]*).+?)$", ingredient_text.strip())):
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
        optional=optional,
        recipe=recipe,
        note=notes or None,
        order=order,
    )


def create_recipe_from_scraper(scraper: AbstractScraper, url: str) -> Recipe | None:
    """Take a scraper and try to create a recipe from it."""
    title = scraper.title()
    host = scraper.host() or urlsplit(url).hostname
    recipe = Recipe(name=title, slug=slugify(title), source_value=url, source=get_or_create_source(host))
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
            for i, instruction in enumerate(scraper.instructions().split("\n"))
            if instruction.strip()
        ],
    )

    # Parse all ingredients
    for i, line in enumerate(scraper.ingredients()):
        parse_ingredient(recipe, line, i + 1)

    recipe.save()
    return recipe
