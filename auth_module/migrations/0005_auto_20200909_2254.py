# Generated by Django 3.1.1 on 2020-09-09 22:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_module', '0004_cinema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinema',
            name='movie',
        ),
        migrations.AddField(
            model_name='cinema',
            name='movie',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, unique=True), blank=True, null=True, size=None),
        ),
    ]
