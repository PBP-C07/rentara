# Generated by Django 5.1.2 on 2024-10-27 09:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='description',
            field=models.TextField(max_length=195),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='title',
            field=models.CharField(max_length=27),
        ),
    ]