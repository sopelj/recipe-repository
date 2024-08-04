"""
Django settings for recipe_repo project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environ import Env

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = BASE_DIR / "recipe_repo"

env = Env()
Env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]


# Application definition
INSTALLED_APPS = [
    # Must be before admin inclusion
    "admin_interface",
    "modeltranslation",
    # Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd Party
    "adminsortable2",
    "cachalot",
    "easy_thumbnails",
    "django_breeze",
    "django_extensions",
    "query_inspector",
    "treebeard",
    "colorfield",
    # Local apps
    "recipe_repo.food",
    "recipe_repo.users",
    "recipe_repo.units",
    "recipe_repo.recipes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "recipe_repo.inertia.middleware.inertia_share",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG or env.bool("DEBUG_QUERIES", default=False):
    MIDDLEWARE.append("query_inspector.middleware.QueryCountMiddleware")

ROOT_URLCONF = "recipe_repo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "recipe_repo.wsgi.application"
ASGI_APPLICATION = "recipe_repo.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {"default": env.db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}

AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

MEDIA_ROOT = str(BASE_DIR / "uploads")
MEDIA_URL = "/uploads/"

# Internationalization
USE_I18N = True
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
    ("ja", _("Japanese")),
)
LOCALE_PATHS = [
    str(APPS_DIR / "locales"),
]
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en", "fr")
MODELTRANSLATION_CUSTOM_FIELDS = ("ArrayField",)

TIME_ZONE = env("TZ", default="America/Montreal")
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Thumbnail Generation
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_ALIASES = {
    "": {
        "profile": {"size": (80, 80), "crop": True},
        "admin": {"size": (100, 100), "crop": True},
        "thumbnail": {"size": (250, 250), "crop": True},
        "photo": {"size": (500, 500), "crop": True},
    },
}

# Debugging
QUERYCOUNT = {
    "IGNORE_ALL_REQUESTS": False,
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 0,
    },
    "DISPLAY_ALL": True,
    "DISPLAY_PRETTIFIED": True,
    "COLOR_FORMATTER_STYLE": "monokai",
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
    "DISPLAY_DUPLICATES": 0,
}

# Caching
if env.bool("MEMCACHED_ENABLED", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": env.cache_url("MEMCACHED_HOST"),
        },
    }


# LDAP Auth
if env.bool("AUTH_LDAP_ENABLED", False):
    AUTH_LDAP_SERVER_URI = env("AUTH_LDAP_SERVER_URI")
    AUTH_LDAP_START_TLS = env.bool("AUTH_LDAP_START_TLS", default=False)
    AUTH_LDAP_BASE_DN = env("AUTH_LDAP_BASE_DN")
    AUTH_LDAP_USER_DN_TEMPLATE = env("AUTH_LDAP_USER_DN_TEMPLATE", default=f"uid=%(user)s,{AUTH_LDAP_BASE_DN}")
    AUTHENTICATION_BACKENDS = (
        "django_auth_ldap.backend.LDAPBackend",
        "django.contrib.auth.backends.ModelBackend",
    )
    if ldap_user_attr_map := env.dict("AUTH_LDAP_USER_ATTR_MAP", default=None):
        AUTH_LDAP_USER_ATTR_MAP = ldap_user_attr_map

    if ldap_user_group_flags := env.dict("AUTH_LDAP_USER_FLAGS_BY_GROUP", default=None):
        AUTH_LDAP_USER_FLAGS_BY_GROUP = ldap_user_group_flags
