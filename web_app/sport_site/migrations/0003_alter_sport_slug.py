# Generated by Django 4.2.9 on 2024-02-04 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_site', '0002_alter_sport_options_sport_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
