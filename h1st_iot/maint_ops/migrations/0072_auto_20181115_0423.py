# Generated by Django 2.1.1 on 2018-11-15 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_MaintOps', '0071_auto_20181115_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='from_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='alert',
            name='has_associated_equipment_problem_diagnoses',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='alert',
            name='ongoing',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='alert',
            name='risk_score_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='alert',
            name='threshold',
            field=models.FloatField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='to_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='blueprint',
            name='trained_to_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='equipmentinstancedailyriskscore',
            name='date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='equipmentinstancedailyriskscore',
            name='risk_score_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='dismissed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='from_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='has_associated_alerts',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='has_equipment_problems',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='equipmentinstanceproblemdiagnosis',
            name='to_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='equipmentproblemtype',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Equipment Problem Type Name'),
        ),
        migrations.AlterField(
            model_name='equipmentuniquetypegroupdatafieldblueprintbenchmarkmetricprofile',
            name='trained_to_date',
            field=models.DateField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name='equipmentuniquetypegroupdatafieldprofile',
            name='to_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentuniquetypegroupmonitoreddatafieldconfig',
            name='active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='equipmentuniquetypegroupserviceconfig',
            name='active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
