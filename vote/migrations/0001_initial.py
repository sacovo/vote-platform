# Generated by Django 3.0.6 on 2020-05-18 14:02

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Delegate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=180)),
                ("last_name", models.CharField(max_length=180)),
                ("birthday", models.DateField()),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=180)),
            ],
        ),
        migrations.CreateModel(
            name="Votation",
            fields=[
                ("title", models.CharField(max_length=180)),
                ("options", models.TextField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("vote", models.CharField(max_length=12)),
                (
                    "delegate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vote.Delegate"
                    ),
                ),
                (
                    "votation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vote.Votation"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="delegate",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="vote.Section"
            ),
        ),
    ]
