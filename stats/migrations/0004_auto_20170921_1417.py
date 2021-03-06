# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_carryxp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CXP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lumpNotPool', models.BooleanField()),
                ('value', models.IntegerField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Character')),
                ('expedition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Expedition')),
            ],
        ),
        migrations.RemoveField(
            model_name='carryxp',
            name='xp_ptr',
        ),
        migrations.DeleteModel(
            name='CarryXP',
        ),
    ]
