# Generated by Django 3.0.6 on 2020-05-18 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_delegate_secret'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delegate',
            name='birthday',
        ),
    ]