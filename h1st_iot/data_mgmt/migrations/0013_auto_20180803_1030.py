# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-03 17:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_DataMgmt', '0012_auto_20180803_0033'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EquipmentEnsemble',
            new_name='EquipmentSystem',
        ),
    ]
