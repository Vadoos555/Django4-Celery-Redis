# Generated by Django 4.2.9 on 2024-02-06 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport_site', '0005_category_sport_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sport_site.category'),
        ),
    ]
