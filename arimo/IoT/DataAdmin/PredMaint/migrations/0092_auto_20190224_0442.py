# Generated by Django 2.1.5 on 2019-02-24 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arimo_IoT_DataAdmin_Base', '0055_auto_20190224_0155'),
        ('Arimo_IoT_DataAdmin_PredMaint', '0091_auto_20190224_0156'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alert',
            unique_together={('equipment_unique_type_group', 'equipment_instance', 'risk_score_name', 'threshold', 'from_date'), ('equipment_unique_type_group', 'equipment_instance', 'risk_score_name', 'threshold', 'to_date')},
        ),
    ]
