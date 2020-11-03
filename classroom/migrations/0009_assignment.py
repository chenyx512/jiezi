# Generated by Django 3.1.1 on 2020-10-31 14:27

from django.db import migrations, models
import django.db.models.deletion
import learning.models.review_manager


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20201028_0837_squashed_0007_delete_reviewmanager'),
        ('learning', '0021_auto_20201031_1427'),
        ('classroom', '0008_auto_20201015_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('character_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='content.characterset')),
                ('in_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='classroom.class')),
                ('review_manager', models.ForeignKey(default=learning.models.review_manager.ReviewManager.get_default_pk, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='learning.reviewmanager')),
            ],
            options={
                'ordering': ['-last_modified_time'],
            },
        ),
    ]
