# Generated by Django 5.0.1 on 2024-01-26 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sentence',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.sentence'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='died_at',
            field=models.DateTimeField(null=True, verbose_name='date last died'),
        ),
    ]
