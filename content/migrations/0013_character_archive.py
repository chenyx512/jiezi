# Generated by Django 3.1.1 on 2020-12-21 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20201221_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='archive',
            field=models.JSONField(default='{}'),
            preserve_default=False,
        ),
    ]
