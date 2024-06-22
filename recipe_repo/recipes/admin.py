from django.contrib import admin
from modeltranslation.admin import TranslationBaseModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category


@admin.register(Category)
class CategoryAdmin(TreeAdmin, TranslationBaseModelAdmin):
    form = movenodeform_factory(Category, exclude=("name", "name_plural", "slug"))
