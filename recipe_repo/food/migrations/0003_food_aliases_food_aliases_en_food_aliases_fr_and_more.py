# Generated by Django 4.2.15 on 2024-08-23 19:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0002_alter_food_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="food",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="food",
            name="aliases_en",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="food",
            name="aliases_fr",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="food",
            name="aliases_ja",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
    ]
