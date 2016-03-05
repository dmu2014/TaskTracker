# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20160210_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disqus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=60)),
                ('body', models.TextField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Item')),
            ],
        ),
    ]