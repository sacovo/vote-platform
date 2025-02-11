# Generated by Django 3.0.6 on 2020-05-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0004_auto_20200518_1515"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="votation",
            options={"ordering": ["start_date"]},
        ),
        migrations.AlterModelOptions(
            name="vote",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="vote",
            name="secret",
            field=models.CharField(
                default="318ee924-7f2d-4f49-9d1d-8507df75153e", max_length=40
            ),
            preserve_default=False,
        ),
    ]
