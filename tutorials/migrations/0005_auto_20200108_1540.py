# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-08 14:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0004_auto_20191216_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutorial',
            old_name='media',
            new_name='media_src',
        ),
    ]
