# Generated by Django 2.2.1 on 2019-05-15 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arimo_IoT_DataAdmin_Base', '0069_auto_20190514_1740'),
        ('Arimo_IoT_DataAdmin_PredMaint', '0101_remove_equipmentproblemtype_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentproblemperiod',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentproblemperiod',
            name='to_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='equipmentproblemperiod',
            unique_together={('equipment_instance', 'from_date'), ('equipment_instance', 'from_date', 'to_date')},
        ),
    ]
