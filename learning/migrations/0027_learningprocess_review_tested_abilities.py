# Generated by Django 3.1.1 on 2020-10-29 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0026_remove_scability_mastered'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningprocess',
            name='review_tested_abilities',
            field=models.ManyToManyField(related_name='_learningprocess_review_tested_abilities_+', to='learning.Ability'),
        ),
    ]
