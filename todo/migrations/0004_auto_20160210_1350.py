# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20160210_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Item'),
        ),
    ]
