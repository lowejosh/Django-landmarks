# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-18 04:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0015_merge_20171018_0411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='longtiude',
            new_name='longitude',
        ),
        migrations.RenameField(
            model_name='locationsuggestion',
            old_name='longtiude',
            new_name='longitude',
        ),
    ]