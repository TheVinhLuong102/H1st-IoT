# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 05:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('H1stIoT_DataMgmt_MaintOps', '0022_equipmentproblemperiod_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentinstanceproblemdiagnosis',
            options={'ordering': ('-from_date', '-to_date', 'equipment_instance')},
        ),
    ]
