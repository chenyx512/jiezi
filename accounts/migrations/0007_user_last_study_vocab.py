# Generated by Django 2.2.1 on 2019-06-15 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_auto_20190504_0528'),
        ('accounts', '0006_user_cn_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_study_vocab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='learning.Character'),
        ),
    ]
