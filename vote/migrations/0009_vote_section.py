# Generated by Django 3.0.6 on 2020-05-21 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0008_auto_20200521_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='section',
            field=models.ForeignKey(default=1,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to='vote.Section'),
            preserve_default=False,
        ),
    ]
