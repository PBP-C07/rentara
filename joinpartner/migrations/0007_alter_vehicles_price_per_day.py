# Generated by Django 5.1.1 on 2024-10-24 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joinpartner', '0006_alter_vehicles_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='price_per_day',
            field=models.IntegerField(),
        ),
    ]
