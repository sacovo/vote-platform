# Generated by Django 3.0.6 on 2020-10-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0021_votation_show_absolute_majority'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='show_end_results',
            field=models.BooleanField(default=False),
        ),
    ]