# Generated by Django 5.0.7 on 2024-08-01 04:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elanlar", "0003_advertisement_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="color",
            field=models.CharField(
                choices=[("RED", "Red"), ("WHITE", "White")], max_length=12
            ),
        ),
    ]
