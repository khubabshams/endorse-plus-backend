# Generated by Django 3.2.19 on 2023-05-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='relationship',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]
