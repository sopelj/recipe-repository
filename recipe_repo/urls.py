"""URL configuration for recipe_repo project."""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="recipes:recipe-list"), name="index"),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("recipe_repo.recipes.urls")),
    path("", include("recipe_repo.categories.urls")),
    path(_("admin/"), admin.site.urls),
    prefix_default_language=True,
)
