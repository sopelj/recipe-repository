# Generated by Django 4.2.14 on 2024-08-07 01:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0007_remove_category_depth_remove_category_numchild_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="favourited_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="favourite_recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Favourited by",
            ),
        ),
    ]
