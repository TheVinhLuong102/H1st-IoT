# Generated by Django 2.2.1 on 2019-05-14 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_MaintOps', '0100_auto_20190514_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentproblemtype',
            name='last_updated',
        ),
    ]
