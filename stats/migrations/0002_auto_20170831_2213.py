# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 02:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='dd_date',
            field=models.DateField(default=datetime.date(9999, 12, 31)),
        ),
        migrations.AddField(
            model_name='character',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('PR', 'Proposed'), ('OM', 'On Mission'), ('DD', 'Dead'), ('DP', 'Departed')], default='AC', max_length=2),
        ),
        migrations.AlterField(
            model_name='expedition',
            name='date',
            field=models.DateField(),
        ),
    ]