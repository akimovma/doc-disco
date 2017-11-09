# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'To Fill'), (1, 'In Progress'), (2, 'Complete')], default=0, verbose_name='Order status'),
        ),
    ]