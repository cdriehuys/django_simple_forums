# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('simple_forums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
