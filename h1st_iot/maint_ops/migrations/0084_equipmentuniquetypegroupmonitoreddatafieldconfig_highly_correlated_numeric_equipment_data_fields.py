# Generated by Django 2.1.5 on 2019-02-01 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_DataMgmt', '0037_auto_20190128_2137'),
        ('IoT_MaintOps', '0083_auto_20190201_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentuniquetypegroupmonitoreddatafieldconfig',
            name='highly_correlated_numeric_equipment_data_fields',
            field=models.ManyToManyField(blank=True, related_name='equipment_unique_type_group_monitored_data_field_configs_high_corr', related_query_name='equipment_unique_type_group_monitored_data_field_config_high_corr', to='IoT_DataMgmt.EquipmentDataField'),
        ),
    ]
