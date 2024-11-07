# Generated by Django 5.1.1 on 2024-11-04 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=100)),
                ("street", models.CharField(blank=True, max_length=100)),
                ("house", models.CharField(blank=True, max_length=20)),
                ("postal_code", models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="city",
        ),
        migrations.AddField(
            model_name="customuser",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.address",
            ),
        ),
    ]