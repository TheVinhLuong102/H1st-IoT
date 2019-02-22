from __future__ import print_function

from django.db.models import \
    Model, \
    BigAutoField, CharField, DateField, DateTimeField, FloatField, IntegerField, TextField, URLField, \
    ForeignKey, ManyToManyField, \
    PROTECT
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import m2m_changed
from django.utils.encoding import python_2_unicode_compatible

import warnings

from ..util import MAX_CHAR_LEN, clean_lower_str, clean_upper_str


@python_2_unicode_compatible
class GlobalConfig(Model):
    key = \
        CharField(
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    value = \
        JSONField(
            blank=True,
            null=True,
            default=None)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = 'key',

    def __str__(self):
        return '{} = {}'.format(self.key, self.value)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.key = clean_upper_str(self.key)

        return super(GlobalConfig, self).save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields)


@python_2_unicode_compatible
class DataType(Model):
    name = \
        CharField(
            verbose_name='Data Type Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'DataTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(DataType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class NumericMeasurementUnit(Model):
    name = \
        CharField(
            verbose_name='Numeric Measurement Unit Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    description = \
        JSONField(
            blank=True,
            null=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return u'NumMeasureUnit "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()   # remove leading & trailing spaces
        return super(NumericMeasurementUnit, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentDataFieldType(Model):
    name = \
        CharField(
            verbose_name='Equipment Data Field Type Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'EqDataFldTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentDataFieldType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentGeneralType(Model):
    name = \
        CharField(
            verbose_name='Equipment General Type Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'EqGenTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentGeneralType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentDataField(Model):
    RELATED_NAME = 'equipment_data_fields'
    RELATED_QUERY_NAME = 'equipment_data_field'

    DEFAULT_UPPER_NUMERIC_NULL = 2 ** 30   # << MaxInt = 2 ** 31 - 1
    DEFAULT_LOWER_NUMERIC_NULL = -DEFAULT_UPPER_NUMERIC_NULL

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_data_field_type = \
        ForeignKey(
            to=EquipmentDataFieldType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    name = \
        CharField(
            verbose_name='Equipment Data Field Name',
            blank=False,
            null=False,
            unique=False,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    data_type = \
        ForeignKey(
            to=DataType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    numeric_measurement_unit = \
        ForeignKey(
            to=NumericMeasurementUnit,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    lower_numeric_null = \
        FloatField(
            blank=False,
            null=False,
            default=DEFAULT_LOWER_NUMERIC_NULL)

    upper_numeric_null = \
        FloatField(
            blank=False,
            null=False,
            default=DEFAULT_UPPER_NUMERIC_NULL)

    default_val = \
        FloatField(
            blank=True,
            null=True)

    min_val = \
        FloatField(
            blank=True,
            null=True)

    max_val = \
        FloatField(
            blank=True,
            null=True)

    description = \
        JSONField(
            blank=True,
            null=True)

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_data_field_type', \
            'name'

        unique_together = \
            'equipment_general_type', \
            'name'
        
    def __str__(self):
        return u'{} [{}] {} [{}{}{}{}{}{}]'.format(
                self.equipment_general_type.name.upper(),
                self.equipment_data_field_type.name,
                self.name,
                self.data_type.name
                    if self.data_type
                    else 'UNTYPED',
                u', unit {}'.format(self.numeric_measurement_unit.name.upper())
                    if self.numeric_measurement_unit and self.numeric_measurement_unit.name
                    else '',
                ('' if self.upper_numeric_null is None
                    else ', null {}'.format(self.upper_numeric_null))
                    if self.lower_numeric_null is None
                    else (', null {}'.format(self.lower_numeric_null)
                          if self.upper_numeric_null is None
                          else ', nulls ({}, {})'.format(self.lower_numeric_null, self.upper_numeric_null)),
                '' if self.default_val is None
                   else ', default {}'.format(self.default_val),
                '' if self.min_val is None
                   else ', min {}'.format(self.min_val),
                '' if self.max_val is None
                   else ', max {}'.format(self.max_val))

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentDataField, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentUniqueTypeGroup(Model):
    RELATED_NAME = 'equipment_unique_type_groups'
    RELATED_QUERY_NAME = 'equipment_unique_type_group'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    name = \
        CharField(
            verbose_name='Equipment Unique Type Group Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    description = \
        JSONField(
            blank=True,
            null=True)

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'name'

    def __str__(self):
        return '{} UnqTpGrp {}'.format(
                self.equipment_general_type.name.upper(),
                self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentUniqueTypeGroup, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentUniqueType(Model):
    RELATED_NAME = 'equipment_unique_types'
    RELATED_QUERY_NAME = 'equipment_unique_type'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    name = \
        CharField(
            verbose_name='Equipment Unique Type Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    description = \
        JSONField(
            blank=True,
            null=True)

    data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            through=EquipmentDataField.equipment_unique_types.through,
            blank=True)

    groups = \
        ManyToManyField(
            to=EquipmentUniqueTypeGroup,
            through=EquipmentUniqueTypeGroup.equipment_unique_types.through,
            blank=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'name'

    def __str__(self):
        return '{} UnqTp {}'.format(
                self.equipment_general_type.name.upper(),
                self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentUniqueType, self).save(*args, **kwargs)


def equipment_unique_types_equipment_data_fields_m2m_changed(
        sender, instance, action, reverse, model, pk_set, using, *args, **kwargs):
    if action == 'pre_add':
        invalid_objs = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(equipment_general_type=instance.equipment_general_type)

        if invalid_objs:
            warnings.warn(
                messsag='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT EQUIPMENT GENERAL TYPE(S) ***'.format(
                        instance, invalid_objs))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs.values('pk'))

    elif action in ('post_add', 'post_remove'):
        if (model is EquipmentDataField) and instance.groups.count():
            equipment_unique_type_groups_to_update = instance.groups.all()

            print('{}: Changed Equipment Data Fields: {}: Updating Equipment Data Fields of {}...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                equipment_unique_type_group_to_update.equipment_data_fields.set(
                    equipment_unique_type_group_to_update.equipment_unique_types.all()[0].data_fields.all().union(
                        *(equipment_unique_type.data_fields.all()
                          for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                        all=False),
                    clear=False)

        elif model is EquipmentUniqueType:
            changed_equipment_unique_types = model.objects.filter(pk__in=pk_set)

            equipment_unique_type_groups_to_update = \
                changed_equipment_unique_types[0].groups.all().union(
                    *(equipment_unique_type.groups.all()
                      for equipment_unique_type in changed_equipment_unique_types[1:]),
                    all=False)

            if equipment_unique_type_groups_to_update:
                print('{}: Changed Equipment Unique Types: {}: Updating Equipment Data Fields of {} Related to Added/Removed {}...'
                    .format(instance, action.upper(), equipment_unique_type_groups_to_update, changed_equipment_unique_types))

                for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0].data_fields.all().union(
                            *(equipment_unique_type.data_fields.all()
                              for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)

    elif action == 'pre_clear':
        if (model is EquipmentDataField) and instance.groups.count():
            equipment_unique_type_groups_to_update = instance.groups.all()

            print('*** {}: CLEARING Equipment Data Fields: {}: Updating Equipment Data Fields of {}... ***'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                remaining_equipment_unique_types = \
                    equipment_unique_type_group_to_update.equipment_unique_types.exclude(pk=instance.pk)

                if remaining_equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        remaining_equipment_unique_types[0].data_fields.all().union(
                            *(remaining_equipment_unique_type.data_fields.all()
                              for remaining_equipment_unique_type in remaining_equipment_unique_types[1:]),
                            all=False),
                        clear=False)

                else:
                    print('*** {}: CLEARING Equipment Data Fields: {}: CLEARING Equipment Data Fields of {}... ***'
                        .format(instance, action.upper(), equipment_unique_type_groups_to_update))

                    equipment_unique_type_group_to_update.equipment_data_fields.clear()

        elif (model is EquipmentUniqueType) and instance.equipment_unique_types.count():
            equipment_unique_types_to_clear = instance.equipment_unique_types.all()

            equipment_unique_type_groups_to_update = \
                equipment_unique_types_to_clear[0].groups.all().union(
                    *(equipment_unique_type_to_clear.groups.all()
                      for equipment_unique_type_to_clear in equipment_unique_types_to_clear[1:]),
                    all=False)

            if equipment_unique_type_groups_to_update:
                print('*** {}: CLEARING Equipment Unique Types: {}: Updating Equipment Data Fields of {} Related to {} to Clear...'
                    .format(instance, action.upper(), equipment_unique_type_groups_to_update, equipment_unique_types_to_clear))

                for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                    first_equipment_unique_type = \
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0]

                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        (first_equipment_unique_type.data_fields.exclude(pk=instance.pk)
                         if first_equipment_unique_type in equipment_unique_types_to_clear
                         else first_equipment_unique_type.data_fields.all()).union(
                            *((equipment_unique_type_group_equipment_unique_type.data_fields.exclude(pk=instance.pk)
                               if equipment_unique_type_group_equipment_unique_type in equipment_unique_types_to_clear
                               else equipment_unique_type_group_equipment_unique_type.data_fields.all())
                              for equipment_unique_type_group_equipment_unique_type in
                                equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)


m2m_changed.connect(
    receiver=equipment_unique_types_equipment_data_fields_m2m_changed,
    sender=EquipmentUniqueType.data_fields.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def equipment_unique_type_groups_equipment_unique_types_m2m_changed(
        sender, instance, action, reverse, model, pk_set, using, *args, **kwargs):
    if action == 'pre_add':
        invalid_objs = \
            model.objects \
                .filter(pk__in=pk_set) \
                .exclude(equipment_general_type=instance.equipment_general_type)

        if invalid_objs:
            warnings.warn(
                messsag='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT EQUIPMENT GENERAL TYPE(S) ***'.format(
                    instance, invalid_objs))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs.values('pk'))

    elif action in ('post_add', 'post_remove'):
        if model is EquipmentUniqueType:
            if instance.equipment_unique_types.count():
                print('{}: Changed Equipment Unique Types: {}: Updating Equipment Data Fields...'
                    .format(instance, action.upper()))

                instance.equipment_data_fields.set(
                    instance.equipment_unique_types.all()[0].data_fields.all().union(
                        *(equipment_unique_type.data_fields.all()
                          for equipment_unique_type in instance.equipment_unique_types.all()[1:]),
                        all=False),
                    clear=False)

            else:
                print('*** {}: REMOVED Equipment Unique Types: {}: CLEARING Equipment Data Fields... ***'
                    .format(instance, action.upper()))

                instance.data_fields.clear()

        elif model is EquipmentUniqueTypeGroup:
            equipment_unique_type_groups_to_update = model.objects.filter(pk__in=pk_set)

            print('{}: Changed Equipment Unique Type Groups: {}: Updating Equipment Data Fields of Added/Removed {}...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                if equipment_unique_type_group_to_update.equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0].data_fields.all().union(
                            *(equipment_unique_type.data_fields.all()
                              for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)

                else:
                    print('*** {}: REMOVED Equipment Unique Types: {}: CLEARING Equipment Data Fields... ***'
                        .format(equipment_unique_type_group_to_update, action.upper()))

                    equipment_unique_type_group_to_update.equipment_data_fields.clear()

    elif action == 'pre_clear':
        if model is EquipmentUniqueType:
            print('*** {}: CLEARING Equipment Unique Types: {}: CLEARING Equipment Data Fields... ***'
                .format(instance, action.upper()))

            instance.equipment_data_fields.clear()

        elif (model is EquipmentUniqueTypeGroup) and instance.groups.count():
            equipment_unique_type_groups_to_update = instance.groups.all()

            print('{}: CLEARING Equipment Unique Type Groups: {}: Updating Equipment Data Fields of {} to Clear...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                remaining_equipment_unique_types = \
                    equipment_unique_type_group_to_update.equipment_unique_types.exclude(pk=instance.pk)

                if remaining_equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        remaining_equipment_unique_types.all()[0].data_fields.all().union(
                            *(equipment_unique_type.data_fields.all()
                              for equipment_unique_type in remaining_equipment_unique_types[1:]),
                            all=False),
                        clear=False)

                else:
                    print('*** {}: REMOVING Equipment Unique Types: {}: CLEARING Equipment Data Fields... ***'
                        .format(equipment_unique_type_group_to_update, action.upper()))

                    equipment_unique_type_group_to_update.equipment_data_fields.clear()


m2m_changed.connect(
    receiver=equipment_unique_type_groups_equipment_unique_types_m2m_changed,
    sender=EquipmentUniqueTypeGroup.equipment_unique_types.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


@python_2_unicode_compatible
class EquipmentFacility(Model):
    RELATED_NAME = 'equipment_facilities'
    RELATED_QUERY_NAME = 'equipment_facility'

    name = \
        CharField(
            verbose_name='Equipment Facility Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    info = \
        JSONField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'EqFacility "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentFacility, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentInstance(Model):
    RELATED_NAME = 'equipment_instances'
    RELATED_QUERY_NAME = 'equipment_instance'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type = \
        ForeignKey(
            to=EquipmentUniqueType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    equipment_facility = \
        ForeignKey(
            to=EquipmentFacility,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    name = \
        CharField(
            verbose_name='Equipment Instance Name',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    info = \
        JSONField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_unique_type', \
            'name'

    def __str__(self):
        return '{}{} #{}'.format(
                self.equipment_general_type.name.upper(),
                ' UnqTp {}'.format(self.equipment_unique_type.name)
                    if self.equipment_unique_type
                    else '',
                self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentInstance, self).save(*args, **kwargs)


class EquipmentInstanceDataFieldDailyAgg(Model):
    RELATED_NAME = 'equipment_instance_data_field_daily_aggs'
    RELATED_QUERY_NAME = 'equipment_instance_data_field_daily_agg'

    id = BigAutoField(
            primary_key=True)

    equipment_instance = \
        ForeignKey(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_data_field = \
        ForeignKey(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_now_add=False,
            db_index=True)

    daily_count = \
        IntegerField(
            blank=False,
            null=False,
            default=0)

    daily_distinct_value_counts = \
        JSONField(
            default=dict,
            encoder=None)

    daily_min = \
        FloatField(
            blank=True,
            null=True)

    daily_outlier_rst_min = \
        FloatField(
            blank=True,
            null=True)

    daily_quartile = \
        FloatField(
            blank=True,
            null=True)

    daily_median = \
        FloatField(
            blank=True,
            null=True)

    daily_mean = \
        FloatField(
            blank=True,
            null=True)

    daily_3rd_quartile = \
        FloatField(
            blank=True,
            null=True)

    daily_outlier_rst_max = \
        FloatField(
            blank=True,
            null=True)

    daily_max = \
        FloatField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)


@python_2_unicode_compatible
class EquipmentSystem(Model):
    RELATED_NAME = 'equipment_systems'
    RELATED_QUERY_NAME = 'equipment_system'

    equipment_facility = \
        ForeignKey(
            to=EquipmentFacility,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    name = \
        CharField(
            verbose_name='Equipment System Name',
            blank=False,
            null=False,
            default=None,
            db_index=True,
            # unique=True,
            max_length=MAX_CHAR_LEN)

    date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_now_add=False,
            db_index=True)

    equipment_instances = \
        ManyToManyField(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'name', \
            'date'

    def __str__(self):
        return '{} on {}'.format(self.name, self.date)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentSystem, self).save(*args, **kwargs)
