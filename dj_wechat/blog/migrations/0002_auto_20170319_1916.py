# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_list',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]