# Generated by Django 2.2.1 on 2019-05-16 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_MaintOps', '0102_auto_20190515_0325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentinstanceproblemdiagnosis',
            options={'ordering': ('-ongoing', '-from_date', '-to_date', 'dismissed')},
        ),
    ]
