from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str | None, password: str, **extra_fields: Any) -> User:
        """Create and save a user with the given email, and password."""
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any):
        """Create user with email."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> User:
        """Create Superuser with email."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model to allow for extra attributes."""

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    email = models.EmailField(_("Email address"), blank=False, unique=True)
    photo = ThumbnailerImageField(_("Photo"), null=True, blank=True)
    language = models.CharField(
        _("Language"),
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        max_length=2,
    )
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts.",
        ),
    )
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    objects = UserManager()

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
        if self.first_name or self.last_name:
            return "".join(name[0] for name in (self.first_name, self.last_name) if name)[:2].upper()
        return self.email[:2].upper()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
