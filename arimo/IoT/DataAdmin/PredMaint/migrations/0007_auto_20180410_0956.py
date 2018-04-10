# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-10 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Arimo_IoT_DataAdmin_Base', '0005_auto_20180103_1059'),
        ('Arimo_IoT_DataAdmin_PredMaint', '0006_auto_20180410_0348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blueprint',
            options={'ordering': ('equipment_general_type', 'equipment_unique_type', 'uuid', 'timestamp')},
        ),
        migrations.AddField(
            model_name='blueprint',
            name='equipment_unique_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='blueprints', related_query_name='blueprint', to='Arimo_IoT_DataAdmin_Base.EquipmentUniqueType'),
        ),
        migrations.AlterField(
            model_name='blueprint',
            name='equipment_general_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='blueprints', related_query_name='blueprint', to='Arimo_IoT_DataAdmin_Base.EquipmentGeneralType'),
        ),
    ]
