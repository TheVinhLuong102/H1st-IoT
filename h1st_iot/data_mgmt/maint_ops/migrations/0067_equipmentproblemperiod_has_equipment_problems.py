# Generated by Django 2.1.1 on 2018-10-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('H1stIoT_DataMgmt_MaintOps', '0066_auto_20181020_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='has_equipment_problems',
            field=models.BooleanField(default=False),
        ),
    ]
