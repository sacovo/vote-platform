# Generated by Django 3.0.4 on 2020-05-20 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_auto_20200520_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='block',
            field=models.CharField(default='A', max_length=20),
            preserve_default=False,
        ),
    ]