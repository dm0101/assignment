# Generated by Django 3.1.1 on 2020-09-09 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_module', '0002_city_movie_showtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=16, null=True, unique=True),
        ),
    ]
