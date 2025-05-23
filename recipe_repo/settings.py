"""
Django settings for recipe_repo project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from django.urls import reverse_lazy
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
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
FORMS_URLFIELD_ASSUME_HTTPS = True

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
    "inertia",
    "django_vite",
    "django_extensions",
    "colorfield",
    # Local apps
    "recipe_repo.categories",
    "recipe_repo.common",
    "recipe_repo.food",
    "recipe_repo.recipes",
    "recipe_repo.users",
    "recipe_repo.units",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "inertia.middleware.InertiaMiddleware",
    "recipe_repo.common.middleware.inertia_share",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if env.bool("QUERY_LOGGING_ENABLED", default=False):
    MIDDLEWARE.append("query_inspector.middleware.QueryCountMiddleware")

ROOT_URLCONF = "recipe_repo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src"],
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
if not (default_db := env.db_url("DATABASE_URL", default=None)):
    default_db = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="recipe_repo"),
        "USER": env("POSTGRES_USER", default="recipe_repo"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_DB_HOST", default="localhost"),
        "PORT": "5432",
    }
DATABASES = {"default": default_db}

AUTH_USER_MODEL = "users.User"
LOGIN_URL = reverse_lazy("admin:login")
LOGIN_REDIRECT_URL = reverse_lazy("recipes:recipe-list")

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
MEDIA_ROOT = str(BASE_DIR / "uploads")
MEDIA_URL = "/uploads/"

STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR / "static")

# Internationalization
USE_I18N = True
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
    ("ja", _("Japanese")),
)
LOCALE_PATHS = [
    APPS_DIR / "locales",
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
        "image": {"size": (600, 600), "crop": True},
    },
}

# Frontend
APP_TITLE = env("VITE_APP_TITLE", default="Recipe Repository")
APP_TITLE_SHORT = env("VITE_APP_TITLE_SHORT", default="Recipes")
APP_THEME_COLOUR = env("VITE_APP_THEME_COLOUR", default="#482880")

# Inertia
INERTIA_VERSION = "2.0"
INERTIA_LAYOUT = "index.html"
INERTIA_SSR_URL = "http://localhost:13714"
INERTIA_SSR_ENABLED = False
INERTIA_ENCRYPT_HISTORY = False

CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"

# Frontend Assets in Dev
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
        "manifest_path": str(BASE_DIR / "dist" / "manifest.json"),
    },
}

STATICFILES_DIRS = [
    BASE_DIR / "dist",
    BASE_DIR / "src" / "assets",
    BASE_DIR / "src" / "public",
]

# Debug Queries
if env.bool("QUERY_LOGGING_ENABLED", default=False):
    INSTALLED_APPS.append("query_inspector")

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
    CACHES = {"default": env.cache_url("MEMCACHED_HOST")}

# Behind Proxy for HTTPS
if env.bool("SSL_ENABLED", False):
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000

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
    if ldap_user_attr_map := env.json("AUTH_LDAP_USER_ATTR_MAP", default=None):
        AUTH_LDAP_USER_ATTR_MAP = ldap_user_attr_map

    if ldap_user_group_flags := env.json("AUTH_LDAP_USER_FLAGS_BY_GROUP", default=None):
        AUTH_LDAP_USER_FLAGS_BY_GROUP = ldap_user_group_flags
        AUTH_LDAP_FIND_GROUP_PERMS = True

# Logging
LOG_LEVEL = env("LOG_LEVEL", default="WARNING")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[DJANGO] %(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s:%(lineno)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
