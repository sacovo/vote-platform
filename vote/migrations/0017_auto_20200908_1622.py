# Generated by Django 3.0.6 on 2020-09-08 16:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0016_auto_20200908_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteset',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='voteset',
            name='votation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='vote.Votation'),
            preserve_default=False,
        ),
    ]