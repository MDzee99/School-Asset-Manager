# Generated by Django 5.2 on 2025-04-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_school_city_school_region_alter_school_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
