from django.db.models import (
    Model,
    BigAutoField, CharField, DateField, FloatField, IntegerField,
    JSONField,
    ForeignKey, ManyToManyField,
    PROTECT)
from django.db.models.signals import m2m_changed, pre_delete

import warnings

from ..util import MAX_CHAR_LEN, clean_lower_str, clean_upper_str


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
            null=True)

    class Meta:
        ordering = 'key',

    def __str__(self):
        return '{} = {}'.format(self.key, self.value)

    def save(self, *args, **kwargs):
        self.key = clean_upper_str(self.key)
        super().save(*args, **kwargs)


class LogicalDataType(Model):
    name = \
        CharField(
            verbose_name='Data Type',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'LogicalDataTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        super().save(*args, **kwargs)


class NumericMeasurementUnit(Model):
    name = \
        CharField(
            verbose_name='Numeric Measurement Unit',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return f'NumMeasureUnit "{self.name}"'

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)


class EquipmentDataFieldType(Model):
    name = \
        CharField(
            verbose_name='Equipment Data Field Type',
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
        super().save(*args, **kwargs)


class EquipmentGeneralType(Model):
    name = \
        CharField(
            verbose_name='Equipment General Type',
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
        super().save(*args, **kwargs)


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

    name = \
        CharField(
            verbose_name='Equipment Data Field',
            blank=False,
            null=False,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    equipment_data_field_type = \
        ForeignKey(
            to=EquipmentDataFieldType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    data_type = \
        ForeignKey(
            to=LogicalDataType,
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

    min_val = \
        FloatField(
            blank=True,
            null=True)

    max_val = \
        FloatField(
            blank=True,
            null=True)

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        unique_together = \
            'equipment_general_type', \
            'name'

        ordering = \
            'equipment_general_type', \
            'name'
        
    def __str__(self):
        return '{} [{}] {} [{}{}{}{}{}]'.format(
                self.equipment_general_type.name.upper(),
                self.equipment_data_field_type.name,
                self.name,
                self.data_type.name
                    if self.data_type
                    else 'UNTYPED',
                f', unit {self.numeric_measurement_unit.name.upper()}'
                    if self.numeric_measurement_unit and self.numeric_measurement_unit.name
                    else '',
                ', nulls ({}, {})'.format(self.lower_numeric_null, self.upper_numeric_null),
                '' if self.min_val is None
                   else ', min {}'.format(self.min_val),
                '' if self.max_val is None
                   else ', max {}'.format(self.max_val))

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        super().save(*args, **kwargs)


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
            verbose_name='Equipment Unique Type Group',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

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
        super().save(*args, **kwargs)


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
            verbose_name='Equipment Unique Type',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            through=EquipmentDataField.equipment_unique_types.through,
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    equipment_unique_type_groups = \
        ManyToManyField(
            to=EquipmentUniqueTypeGroup,
            through=EquipmentUniqueTypeGroup.equipment_unique_types.through,
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

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
        super().save(*args, **kwargs)


def equipment_unique_types_equipment_data_fields_m2m_changed(
        sender, instance, action, reverse, model, pk_set, using, *args, **kwargs):
    if action == 'pre_add':
        invalid_objs = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(equipment_general_type=instance.equipment_general_type)

        if invalid_objs:
            warnings.warn(
                message='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT EQUIPMENT GENERAL TYPE(S) ***'.format(
                        instance, invalid_objs))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs.values('pk'))

    elif action in ('post_add', 'post_remove') and pk_set:
        if (model is EquipmentDataField) and instance.equipment_unique_type_groups.count():
            equipment_unique_type_groups_to_update = instance.equipment_unique_type_groups.all()

            print('{}: Changed Equipment Data Fields: {}: Updating Equipment Data Fields of {}...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                equipment_unique_type_group_to_update.equipment_data_fields.set(
                    equipment_unique_type_group_to_update.equipment_unique_types.all()[0].equipment_data_fields.all().union(
                        *(equipment_unique_type.equipment_data_fields.all()
                          for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                        all=False),
                    clear=False)

        elif model is EquipmentUniqueType:
            changed_equipment_unique_types = model.objects.filter(pk__in=pk_set)

            equipment_unique_type_groups_to_update = \
                changed_equipment_unique_types[0].equipment_unique_type_groups.all().union(
                    *(equipment_unique_type.equipment_unique_type_groups.all()
                      for equipment_unique_type in changed_equipment_unique_types[1:]),
                    all=False)

            if equipment_unique_type_groups_to_update:
                print('{}: Changed Equipment Unique Types: {}: Updating Equipment Data Fields of {} Related to Added/Removed {}...'
                    .format(instance, action.upper(), equipment_unique_type_groups_to_update, changed_equipment_unique_types))

                for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0].equipment_data_fields.all().union(
                            *(equipment_unique_type.equipment_data_fields.all()
                              for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)

    elif action == 'pre_clear':
        if (model is EquipmentDataField) and instance.equipment_unique_type_groups.count():
            equipment_unique_type_groups_to_update = instance.equipment_unique_type_groups.all()

            print('*** {}: CLEARING Equipment Data Fields: {}: Updating Equipment Data Fields of {}... ***'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                remaining_equipment_unique_types = \
                    equipment_unique_type_group_to_update.equipment_unique_types.exclude(pk=instance.pk)

                if remaining_equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        remaining_equipment_unique_types[0].equipment_data_fields.all().union(
                            *(remaining_equipment_unique_type.equipment_data_fields.all()
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
                equipment_unique_types_to_clear[0].equipment_unique_type_groups.all().union(
                    *(equipment_unique_type_to_clear.equipment_unique_type_groups.all()
                      for equipment_unique_type_to_clear in equipment_unique_types_to_clear[1:]),
                    all=False)

            if equipment_unique_type_groups_to_update:
                print('*** {}: CLEARING Equipment Unique Types: {}: Updating Equipment Data Fields of {} Related to {} to Clear...'
                    .format(instance, action.upper(), equipment_unique_type_groups_to_update, equipment_unique_types_to_clear))

                for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                    first_equipment_unique_type = \
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0]

                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        (first_equipment_unique_type.equipment_data_fields.exclude(pk=instance.pk)
                         if first_equipment_unique_type in equipment_unique_types_to_clear
                         else first_equipment_unique_type.equipment_data_fields.all()).union(
                            *((equipment_unique_type_group_equipment_unique_type.equipment_data_fields.exclude(pk=instance.pk)
                               if equipment_unique_type_group_equipment_unique_type in equipment_unique_types_to_clear
                               else equipment_unique_type_group_equipment_unique_type.equipment_data_fields.all())
                              for equipment_unique_type_group_equipment_unique_type in
                                equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)


m2m_changed.connect(
    receiver=equipment_unique_types_equipment_data_fields_m2m_changed,
    sender=EquipmentUniqueType.equipment_data_fields.through,
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
                message='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT EQUIPMENT GENERAL TYPE(S) ***'.format(
                    instance, invalid_objs))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs.values('pk'))

    elif action in ('post_add', 'post_remove') and pk_set:
        if model is EquipmentUniqueType:
            if instance.equipment_unique_types.count():
                print('{}: Changed Equipment Unique Types: {}: Updating Data Fields...'
                    .format(instance, action.upper()))

                instance.equipment_data_fields.set(
                    instance.equipment_unique_types.all()[0].equipment_data_fields.all().union(
                        *(equipment_unique_type.equipment_data_fields.all()
                          for equipment_unique_type in instance.equipment_unique_types.all()[1:]),
                        all=False),
                    clear=False)

            else:
                print('*** {}: REMOVED Equipment Unique Types: {}: CLEARING Data Fields... ***'
                    .format(instance, action.upper()))

                instance.equipment_data_fields.clear()

        elif model is EquipmentUniqueTypeGroup:
            equipment_unique_type_groups_to_update = model.objects.filter(pk__in=pk_set)

            print('{}: Changed Equipment Unique Type Groups: {}: Updating Data Fields of Added/Removed {}...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                if equipment_unique_type_group_to_update.equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        equipment_unique_type_group_to_update.equipment_unique_types.all()[0].equipment_data_fields.all().union(
                            *(equipment_unique_type.equipment_data_fields.all()
                              for equipment_unique_type in equipment_unique_type_group_to_update.equipment_unique_types.all()[1:]),
                            all=False),
                        clear=False)

                else:
                    print('*** {}: REMOVED Equipment Unique Types: {}: CLEARING Data Fields... ***'
                        .format(equipment_unique_type_group_to_update, action.upper()))

                    equipment_unique_type_group_to_update.equipment_data_fields.clear()

    elif action == 'pre_clear':
        if model is EquipmentUniqueType:
            print('*** {}: CLEARING Equipment Unique Types: {}: CLEARING Data Fields... ***'
                .format(instance, action.upper()))

            instance.equipment_data_fields.clear()

        elif (model is EquipmentUniqueTypeGroup) and instance.equipment_unique_type_groups.count():
            equipment_unique_type_groups_to_update = instance.equipment_unique_type_groups.all()

            print('{}: CLEARING Equipment Unique Type Groups: {}: Updating Data Fields of {} to Clear...'
                .format(instance, action.upper(), equipment_unique_type_groups_to_update))

            for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
                remaining_equipment_unique_types = \
                    equipment_unique_type_group_to_update.equipment_unique_types.exclude(pk=instance.pk)

                if remaining_equipment_unique_types.count():
                    equipment_unique_type_group_to_update.equipment_data_fields.set(
                        remaining_equipment_unique_types.all()[0].equipment_data_fields.all().union(
                            *(equipment_unique_type.equipment_data_fields.all()
                              for equipment_unique_type in remaining_equipment_unique_types[1:]),
                            all=False),
                        clear=False)

                else:
                    print('*** {}: REMOVING Equipment Unique Types: {}: CLEARING Data Fields... ***'
                        .format(equipment_unique_type_group_to_update, action.upper()))

                    equipment_unique_type_group_to_update.equipment_data_fields.clear()


m2m_changed.connect(
    receiver=equipment_unique_type_groups_equipment_unique_types_m2m_changed,
    sender=EquipmentUniqueTypeGroup.equipment_unique_types.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def equipment_unique_type_pre_delete(sender, instance, using, *args, **kwargs):
    if instance.equipment_unique_type_groups.count():
        equipment_unique_type_groups_to_update = instance.equipment_unique_type_groups.all()

        print('*** DELETING {}: Updating Data Streams of {}... ***'
            .format(instance, equipment_unique_type_groups_to_update))

        for equipment_unique_type_group_to_update in equipment_unique_type_groups_to_update:
            remaining_equipment_unique_types = \
                equipment_unique_type_groups_to_update.equipment_unique_types.exclude(pk=instance.pk)

            if remaining_equipment_unique_types.count():
                equipment_unique_type_group_to_update.equipment_data_fields.set(
                    remaining_equipment_unique_types.all()[0].equipment_data_fields.all().union(
                        *(equipment_unique_type.equipment_data_fields.all()
                          for equipment_unique_type in remaining_equipment_unique_types[1:]),
                        all=False),
                    clear=False)

            else:
                print('*** DELETING {}: CLEARING Data Streams of {}... ***'
                    .format(instance, equipment_unique_type_group_to_update))

                equipment_unique_type_group_to_update.equipment_data_fields.clear()


pre_delete.connect(
    receiver=equipment_unique_type_pre_delete,
    sender=EquipmentUniqueType,
    weak=True,
    dispatch_uid=None,
    apps=None)


class EquipmentFacility(Model):
    RELATED_NAME = 'equipment_facilities'
    RELATED_QUERY_NAME = 'equipment_facility'

    name = \
        CharField(
            verbose_name='Equipment Facility',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    info = \
        JSONField(
            blank=True,
            null=True)

    class Meta:
        verbose_name_plural = 'Equipment Facilities'

        ordering = 'name',

    def __str__(self):
        return 'EqFacility "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        super().save(*args, **kwargs)


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
            verbose_name='Equipment Instance',
            blank=False,
            null=False,
            unique=True,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    info = \
        JSONField(
            blank=True,
            null=True)

    equipment_unique_type_groups = \
        ManyToManyField(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

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

        if self.equipment_unique_type and \
                (self.equipment_unique_type.equipment_general_type != self.equipment_general_type):
            warnings.warn(
                message='*** EQUIPMENT INSTANCE #{}: EQUIPMENT UNIQUE TYPE {} NOT OF EQUIPMENT GENERAL TYPE {} ***'
                    .format(self.name, self.equipment_unique_type, self.equipment_general_type))

            self.equipment_unique_type = None

        super().save(*args, **kwargs)


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
            verbose_name='Equipment System',
            blank=False,
            null=False,
            default=None,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    date = \
        DateField(
            blank=False,
            null=False,
            db_index=True)

    equipment_instances = \
        ManyToManyField(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        unique_together = \
            'name', \
            'date'

        ordering = \
            'equipment_facility', \
            'name', \
            'date'

    def __str__(self):
        return '{}{} on {}'.format(
                self.name,
                ' @ EqFacility "{}"'.format(self.equipment_facility.name)
                    if self.equipment_facility
                    else '',
                self.date)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        super().save(*args, **kwargs)


class EquipmentUniqueTypeGroupDataFieldProfile(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_profiles'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_profile'

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
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

    to_date = \
        DateField(
            blank=True,
            null=True,
            db_index=True)

    valid_proportion = \
        FloatField(
            blank=False,
            null=False)

    n_distinct_values = \
        IntegerField(
            blank=False,
            null=False)

    distinct_values = \
        JSONField(
            blank=True,
            null=True)

    sample_min = \
        FloatField(
            blank=True,
            null=True)

    outlier_rst_min = \
        FloatField(
            blank=True,
            null=True)

    sample_quartile = \
        FloatField(
            blank=True,
            null=True)

    sample_median = \
        FloatField(
            blank=True,
            null=True)

    sample_3rd_quartile = \
        FloatField(
            blank=True,
            null=True)

    outlier_rst_max = \
        FloatField(
            blank=True,
            null=True)

    sample_max = \
        FloatField(
            blank=True,
            null=True)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'to_date'

        ordering = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            '-to_date'


class EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_pairwise_correlations'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_pairwise_correlation'

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
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

    equipment_data_field_2 = \
        ForeignKey(
            to=EquipmentDataField,
            blank=False,
            null=False,
            on_delete=PROTECT)

    sample_correlation = \
        FloatField(
            blank=False,
            null=False)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'equipment_data_field_2'

        ordering = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'equipment_data_field_2'
