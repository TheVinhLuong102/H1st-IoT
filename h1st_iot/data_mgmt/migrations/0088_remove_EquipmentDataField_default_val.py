"""Remove EquipmentDataField default_val."""


# pylint: disable=invalid-name


from django.db import migrations


class Migration(migrations.Migration):
    """Remove EquipmentDataField default_val."""

    dependencies = [
        ('H1stIoT_DataMgmt_Base',
         '0087_delete_EquipmentInstanceDataFieldDailyAgg')
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentdatafield',
            name='default_val')
    ]
