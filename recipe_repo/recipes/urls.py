from django.urls import path

from .views import category_list

app_name = "recipes"

urlpatterns = [
    path("", category_list, name="category-list"),
]
