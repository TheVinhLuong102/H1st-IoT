# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-21 23:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arimo_IoT_DataAdmin_PredMaint', '0026_auto_20180721_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='equipment_problem_periods',
            new_name='problems',
        ),
    ]
