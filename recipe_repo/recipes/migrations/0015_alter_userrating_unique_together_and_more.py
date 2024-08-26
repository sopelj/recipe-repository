# Generated by Django 4.2.15 on 2024-08-26 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_migrate_categories"),
        ("recipes", "0014_alter_category_name_alter_category_name_en_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userrating",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="userrating",
            name="recipe",
        ),
        migrations.RemoveField(
            model_name="userrating",
            name="user",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="favourited_by",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="rated_by",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                related_name="recipes",
                to="categories.category",
                verbose_name="Categories",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                related_name="recipes",
                to="categories.category",
                verbose_name="Categories",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="recipes.source",
                verbose_name="Source",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="yield_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="recipes.yieldunit",
            ),
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.DeleteModel(
            name="UserRating",
        ),
    ]
