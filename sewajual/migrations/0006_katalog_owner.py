# Generated by Django 5.1.1 on 2024-10-27 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joinpartner', '0002_vehicles_bahan_bakar'),
        ('sewajual', '0005_merge_20241027_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='katalog',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='joinpartner.partner'),
        ),
    ]
