# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-31 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0017_merge_20171030_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Map',
        ),
        migrations.AlterField(
            model_name='locationsuggestion',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='locationsuggestion',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
