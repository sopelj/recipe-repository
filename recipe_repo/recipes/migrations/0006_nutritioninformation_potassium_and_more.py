# Generated by Django 4.2.14 on 2024-07-29 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_alter_nutritioninformation_recipe"),
    ]

    operations = [
        migrations.AddField(
            model_name="nutritioninformation",
            name="potassium",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="in milligrams",
                null=True,
                verbose_name="Potassium",
            ),
        ),
        migrations.AlterField(
            model_name="nutritioninformation",
            name="cholesterol",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="in milligrams",
                null=True,
                verbose_name="Cholesterol",
            ),
        ),
        migrations.AlterField(
            model_name="nutritioninformation",
            name="sodium",
            field=models.PositiveIntegerField(blank=True, help_text="in milligrams", null=True, verbose_name="Sodium"),
        ),
    ]
