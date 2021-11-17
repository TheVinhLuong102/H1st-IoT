# Generated by Django 2.2.1 on 2019-05-14 03:17

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('H1stIoT_DataMgmt_Base', '0063_auto_20190511_0024'),
        ('H1stIoT_DataMgmt_MaintOps', '0094_auto_20190513_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='equipment_problem_diagnoses',
            new_name='equipment_instance_problem_diagnoses',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='has_associated_equipment_problem_diagnoses',
            new_name='has_associated_equipment_instance_problem_diagnoses',
        ),
        migrations.RenameField(
            model_name='equipmentinstanceproblemdiagnosis',
            old_name='alerts',
            new_name='alert_periods',
        ),
        migrations.RenameField(
            model_name='equipmentinstanceproblemdiagnosis',
            old_name='has_associated_alerts',
            new_name='has_associated_equipment_instance_alert_periods',
        ),
        migrations.AddField(
            model_name='alert',
            name='has_associated_equipment_instance_alarm_periods',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='has_associated_equipment_instance_alarm_periods',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='alert',
            name='equipment_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_instance_alert_periods', related_query_name='equipment_instance_alert_period', to='H1stIoT_DataMgmt_Base.EquipmentInstance'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='equipment_unique_type_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_instance_alert_periods', related_query_name='equipment_instance_alert_period', to='H1stIoT_DataMgmt_Base.EquipmentUniqueTypeGroup'),
        ),
        migrations.CreateModel(
            name='EquipmentInstanceAlarmPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_utc_date_time', models.DateTimeField(db_index=True)),
                ('to_utc_date_time', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('duration_in_days', models.FloatField(blank=True, db_index=True, null=True)),
                ('date_range', django.contrib.postgres.fields.ranges.DateRangeField(blank=True, null=True)),
                ('has_associated_equipment_instance_alert_periods', models.BooleanField(db_index=True, default=False)),
                ('has_associated_equipment_instance_problem_diagnoses', models.BooleanField(db_index=True, default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('alarm_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_instance_alarm_periods', related_query_name='equipment_instance_alarm_period', to='H1stIoT_DataMgmt_MaintOps.EquipmentProblemType')),
                ('equipment_instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_instance_alarm_periods', related_query_name='equipment_instance_alarm_period', to='H1stIoT_DataMgmt_Base.EquipmentInstance')),
                ('equipment_instance_alert_periods', models.ManyToManyField(blank=True, related_name='equipment_instance_alarm_periods', related_query_name='equipment_instance_alarm_period', to='H1stIoT_DataMgmt_MaintOps.Alert')),
                ('equipment_instance_problem_diagnoses', models.ManyToManyField(blank=True, related_name='equipment_instance_alarm_periods', related_query_name='equipment_instance_alarm_period', to='H1stIoT_DataMgmt_MaintOps.EquipmentInstanceProblemDiagnosis')),
            ],
            options={
                'ordering': ('equipment_instance', 'alarm_type', 'from_utc_date_time'),
                'unique_together': {('equipment_instance', 'alarm_type', 'from_utc_date_time', 'to_utc_date_time'), ('equipment_instance', 'alarm_type', 'from_utc_date_time')},
            },
        ),
        migrations.AddField(
            model_name='alert',
            name='alarm_periods',
            field=models.ManyToManyField(blank=True, to='H1stIoT_DataMgmt_MaintOps.EquipmentInstanceAlarmPeriod'),
        ),
        migrations.AddField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='alarm_periods',
            field=models.ManyToManyField(blank=True, to='H1stIoT_DataMgmt_MaintOps.EquipmentInstanceAlarmPeriod'),
        ),
    ]
