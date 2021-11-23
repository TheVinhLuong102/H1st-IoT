# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-31 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_DataMgmt', '0014_auto_20180803_1031'),
        ('IoT_MaintOps', '0032_auto_20180722_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentUniqueTypeGroupMeasurementDataFieldBlueprintBenchmarkMetricProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_date', models.DateField(default=None)),
                ('n', models.IntegerField(default=0)),
                ('mae', models.FloatField(blank=True, null=True)),
                ('medae', models.FloatField(blank=True, null=True)),
                ('r2', models.FloatField(blank=True, null=True)),
                ('last_updated', models.DateTimeField()),
                ('equipment_data_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profile', to='IoT_DataMgmt.EquipmentDataField')),
                ('equipment_general_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profile', to='IoT_DataMgmt.EquipmentGeneralType')),
                ('equipment_unique_type_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_measurement_data_field_benchmark_metric_profile', to='IoT_DataMgmt.EquipmentUniqueTypeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentUniqueTypeGroupMeasurementDataFieldProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_date', models.DateField(default=None)),
                ('valid_proportion', models.FloatField(default=0)),
                ('sample_min', models.FloatField(blank=True, null=True)),
                ('outlier_rst_min', models.FloatField(blank=True, null=True)),
                ('sample_quartile', models.FloatField(blank=True, null=True)),
                ('sample_median', models.FloatField(blank=True, null=True)),
                ('sample_3rd_quartile', models.FloatField(blank=True, null=True)),
                ('outlier_rst_max', models.FloatField(blank=True, null=True)),
                ('sample_max', models.FloatField(blank=True, null=True)),
                ('last_updated', models.DateTimeField()),
                ('equipment_data_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_profile', to='IoT_DataMgmt.EquipmentDataField')),
                ('equipment_general_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_profile', to='IoT_DataMgmt.EquipmentGeneralType')),
                ('equipment_unique_type_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_measurement_data_field_profiles', related_query_name='equipment_unique_type_group_measurement_data_field_profile', to='IoT_DataMgmt.EquipmentUniqueTypeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentUniqueTypeGroupServiceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('equipment_general_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_service_configs', related_query_name='equipment_unique_type_group_service_config', to='IoT_DataMgmt.EquipmentGeneralType')),
                ('equipment_unique_type_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_unique_type_group_service_configs', related_query_name='equipment_unique_type_group_service_config', to='IoT_DataMgmt.EquipmentUniqueTypeGroup')),
            ],
        ),
        migrations.AlterField(
            model_name='alert',
            name='diagnosis_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='IoT_MaintOps.AlertDiagnosisStatus'),
        ),
    ]
