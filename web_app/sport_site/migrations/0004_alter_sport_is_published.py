# Generated by Django 4.2.9 on 2024-02-04 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_site', '0003_alter_sport_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'draft'), (1, 'published')], default=1),
        ),
    ]