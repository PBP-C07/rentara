# Generated by Django 5.1.2 on 2024-10-24 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='notelp',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
