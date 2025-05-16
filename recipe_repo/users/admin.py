from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, User, UserRating

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


class UserAddForm(BaseUserCreationForm[User]):  # type: ignore[type-var]
    class Meta:
        model = User
        fields = ("email",)


@admin.register(User)
class UserAdmin(BaseUserAdmin[User]):  # type: ignore[type-var]
    add_form = UserAddForm
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "photo")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin[UserRating]):
    list_display = ("get_user_full_name", "get_recipe_name", "rating")
    list_filter = [("user", admin.RelatedOnlyFieldListFilter), ("recipe", admin.RelatedOnlyFieldListFilter)]
    autocomplete_fields = ("user", "recipe")

    @admin.display(  # type: ignore[call-overload,misc]
        description=_("User"),
        ordering=("user__first_name", "user__last_name"),
    )
    def get_user_full_name(self, obj: UserRating) -> str:
        """Get full name of user for list view."""
        return obj.user.full_name or obj.user.email

    @admin.display(description=_("Recipe"), ordering=("recipe__name",))  # type: ignore[call-overload,misc]
    def get_recipe_name(self, obj: UserRating) -> str:
        """Get the name of a recipe for list view."""
        return obj.recipe.name

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserRating]:
        """Pre-fetch some fields in list mode."""
        if request.resolver_match and request.resolver_match.view_name == "admin:food_food_changelist":
            return UserRating.objects.select_related("user", "recipe")
        return UserRating.objects.filter()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin[Comment]):
    list_filter = (
        ("user", admin.RelatedOnlyFieldListFilter),
        ("recipe", admin.RelatedOnlyFieldListFilter),
    )
    list_display = ("__str__", "user", "recipe", "created")
    autocomplete_fields = ("user", "recipe")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Comment]:
        """Include related fields to avoid extra queries."""
        return Comment.objects.select_related("user", "recipe")

    def has_change_permission(self, request: HttpRequest, obj: Comment | None = None) -> bool:
        """Allow users to edit their own comments."""
        if obj and obj.user == request.user:
            return True
        return super().has_change_permission(request, obj)
