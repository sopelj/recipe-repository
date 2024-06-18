from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("Email address"), blank=True, unique=True)
    language = models.CharField(
        _("Language"),
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        max_length=2,
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self) -> str:
        return "".join(
            name[0] for name in (self.first_name, self.last_name, self.username) if name
        )[:2].upper()
