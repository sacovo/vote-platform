# Generated by Django 3.0.6 on 2020-06-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0011_auto_20200521_1012"),
    ]

    operations = [
        migrations.AddField(
            model_name="votation",
            name="description",
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
