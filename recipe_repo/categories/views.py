from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ..common.views import InertiaView
from .models import CategoryType
from .serializers import CategoryListSerializer, CategoryTypeListSerializer, CategoryTypeSerializer


class CategoryTypeListView(LoginRequiredMixin, InertiaView):
    component = "CategoryTypeList"

    def get_component_props(self) -> dict[str, Any]:
        """Return categories."""
        return {
            "categoryTypes": CategoryTypeListSerializer(CategoryType.objects.all(), many=True).data,
        }


class CategoryListView(LoginRequiredMixin, InertiaView):
    component = "CategoryList"

    def get_component_props(self) -> dict[str, Any]:
        """Return categories."""
        category_type = get_object_or_404(
            CategoryType.objects.prefetch_related("categories"),
            slug=self.kwargs["category_type_slug"],
        )
        return {
            "categoryType": CategoryTypeSerializer(category_type).data,
            "categories": CategoryListSerializer(category_type.categories.all(), many=True).data,
        }
