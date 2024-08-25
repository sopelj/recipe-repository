# Generated by Django 4.2.15 on 2024-08-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0013_category_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_fr",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_ja",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="ingredientgroup",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="ingredientgroup",
            name="name_en",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="ingredientgroup",
            name="name_fr",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="ingredientgroup",
            name="name_ja",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name_en",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name_fr",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name_ja",
            field=models.CharField(max_length=150, null=True, verbose_name="Name"),
        ),
        migrations.AlterUniqueTogether(
            name="ingredientgroup",
            unique_together={("name", "recipe")},
        ),
    ]
