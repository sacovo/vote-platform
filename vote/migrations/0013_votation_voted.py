# Generated by Django 3.0.6 on 2020-06-23 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0012_votation_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='voted',
            field=models.ManyToManyField(blank=True, to='vote.Delegate'),
        ),
    ]
