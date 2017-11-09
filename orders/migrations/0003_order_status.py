# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20171108_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'To fill'), (1, 'In progress'), (2, 'Complete')], default=0, verbose_name='Order status'),
        ),
    ]
