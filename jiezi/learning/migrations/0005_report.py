# Generated by Django 2.1.7 on 2019-05-04 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('learning', '0004_remove_character_small_color_coded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=100)),
                ('description_1', models.CharField(max_length=100)),
                ('description_2', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserCharacter')),
            ],
        ),
    ]
