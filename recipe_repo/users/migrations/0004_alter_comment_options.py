# Generated by Django 4.2.15 on 2024-08-30 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("-created",), "verbose_name": "Comment", "verbose_name_plural": "Comments"},
        ),
    ]
