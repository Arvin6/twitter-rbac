# Generated by Django 3.1.5 on 2021-01-14 19:53

from django.db import migrations, models
import tweet.utils


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0013_auto_20210114_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='action',
            field=models.CharField(choices=[('CREATE', tweet.utils.LogActions['create']), ('DELETE', tweet.utils.LogActions['delete']), ('UPDATE', tweet.utils.LogActions['update']), ('VIEW', tweet.utils.LogActions['view'])], max_length=10),
        ),
        migrations.AlterField(
            model_name='logs',
            name='action_type',
            field=models.CharField(choices=[('AUDIT', tweet.utils.LogTypes['audit']), ('ACTION', tweet.utils.LogTypes['action']), ('ACCESS', tweet.utils.LogTypes['access'])], max_length=10),
        ),
    ]