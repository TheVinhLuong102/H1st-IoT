# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-31 21:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arimo_IoT_DataAdmin_PredMaint', '0036_auto_20180831_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentuniquetypegroupdatafieldblueprintbenchmarkmetricprofile',
            options={'ordering': ('equipment_general_type', 'equipment_unique_type_group', 'equipment_data_field', '-trained_to_date')},
        ),
        migrations.RenameField(
            model_name='equipmentuniquetypegroupdatafieldblueprintbenchmarkmetricprofile',
            old_name='to_date',
            new_name='trained_to_date',
        ),
    ]
