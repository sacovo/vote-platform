# Generated by Django 3.0.6 on 2020-09-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0014_auto_20200908_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='allow_intermediate',
            field=models.BooleanField(default=True),
        ),
    ]