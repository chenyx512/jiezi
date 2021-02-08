# Generated by Django 3.1.1 on 2021-02-06 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0056_radical_is_learnable'),
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='question_data',
        ),
        migrations.RemoveField(
            model_name='record',
            name='question_is_correct',
        ),
        migrations.AddField(
            model_name='record',
            name='action',
            field=models.SmallIntegerField(choices=[(1, 'Wrong Answer'), (2, 'Correct Answer'), (3, 'Learn'), (4, 'Relearn')], default=0),
        ),
        migrations.AddField(
            model_name='record',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='record',
            name='reviewable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.reviewableobject'),
        ),
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.generalquestion'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(help_text='None means AnonymousUsers', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserReviewable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('learned_related_reviewables', models.ManyToManyField(related_name='_userreviewable_learned_related_reviewables_+', to='content.ReviewableObject')),
                ('reviewable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.reviewableobject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearningProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_id', models.UUIDField(default=uuid.uuid4)),
                ('state_type', models.CharField(default='decide', max_length=20)),
                ('data', models.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wordset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.wordset')),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='learning_process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learning.learningprocess'),
        ),
    ]
