from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer


class User(AbstractUser):
    """Custom user model to allow for extra attributes."""

    email = models.EmailField(_("Email address"), blank=True, unique=True)
    photo = ThumbnailerImageField(_("Photo"), null=True, blank=True)
    language = models.CharField(
        _("Language"),
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        max_length=2,
    )

    @property
    def profile_image_url(self) -> str | None:
        """Resolve URL of the user's profile image."""
        return get_thumbnailer(self.photo)["profile"].url if self.photo else None

    @property
    def full_name(self) -> str:
        """Shortcut for formatting first and last name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self) -> str:
        """Shortcut for formatting initials."""
        return "".join(name[0] for name in (self.first_name, self.last_name, self.username) if name)[:2].upper()

    def serialize(self) -> dict[str, Any]:
        """Serialize the user to a dictionary including extra attributes."""
        return model_to_dict(self, exclude=("password", "groups", "photo")) | {
            "profile_image_url": self.profile_image_url,
        }

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
