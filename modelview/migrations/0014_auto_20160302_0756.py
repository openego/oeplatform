# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 06:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelview', '0013_auto_20160301_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicfactsheet',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='basicfactsheet',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='energymodel',
            name='energy_sectors_oil',
        ),
        migrations.RemoveField(
            model_name='energyscenario',
            name='modeled_energy_sectors_oil',
        ),
    ]