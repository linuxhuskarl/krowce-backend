# Generated by Django 5.0.1 on 2024-01-26 22:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_item_sentence_alter_user_died_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='x',
            field=models.FloatField(verbose_name='distance <0, >'),
        ),
        migrations.AlterField(
            model_name='item',
            name='y',
            field=models.FloatField(verbose_name='height <-4, 4>'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.utcnow, verbose_name='date created'),
        ),
    ]
