# Generated by Django 5.1.5 on 2025-03-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0014_remove_ad_createdimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Город'),
        ),
    ]
