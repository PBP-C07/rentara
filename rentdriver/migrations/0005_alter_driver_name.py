# Generated by Django 5.1.2 on 2024-10-24 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentdriver', '0004_alter_driver_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
