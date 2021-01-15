# Generated by Django 3.1.5 on 2021-01-14 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tweet.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0004_auto_20210111_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[(tweet.models.AdminActions['create'], 'CREATE'), (tweet.models.AdminActions['delete'], 'DELETE'), (tweet.models.AdminActions['update'], 'UPDATE')], max_length=10)),
                ('tweet_content', models.CharField(blank=True, default='', max_length=280)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='action_created_by', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='tweet_created_for', to=settings.AUTH_USER_MODEL)),
                ('tweet_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='tweet.tweet')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='action_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]