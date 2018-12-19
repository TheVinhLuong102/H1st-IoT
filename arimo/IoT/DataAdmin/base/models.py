from django.db.models import \
    Model, \
    BigAutoField, CharField, DateField, DateTimeField, FloatField, IntegerField, URLField, \
    ForeignKey, ManyToManyField, \
    PROTECT
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from ..util import MAX_CHAR_LEN, clean_lower_str


@python_2_unicode_compatible
class DataType(Model):
    name = \
        CharField(
            verbose_name='Data Type Name',
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'NumMeasureUnit "{}"'.format(self.name)


@python_2_unicode_compatible
class EquipmentDataFieldType(Model):
    name = \
        CharField(
            verbose_name='Equipment Data Field Type Name',
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=False,
            db_index=True)

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

    def __str__(self):
        return '{} [{}] {} [{}{}{}{}{}{}]'.format(
                self.equipment_general_type.name.upper(),
                self.equipment_data_field_type.name,
                self.name,
                self.data_type.name
                    if self.data_type
                    else 'UNTYPED',
                ('' if self.numeric_measurement_unit is None
                    else ', unit {}'.format(self.numeric_measurement_unit.name.upper())),
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


def equipment_data_field_post_save(sender, instance, *args, **kwargs):
    for equipment_unique_type in instance.equipment_unique_types.all():
        for equipment_unique_type_group in equipment_unique_type.groups.all():
            equipment_unique_type_group.save()


post_save.connect(
    receiver=equipment_data_field_post_save,
    sender=EquipmentDataField,
    weak=True,
    dispatch_uid=None)


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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

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


def equipment_unique_type_group_post_save(sender, instance, *args, **kwargs):
    if instance.equipment_unique_types.count():
        instance.equipment_data_fields.set(
            instance.equipment_unique_types.all()[0].data_fields.all().union(
                *(equipment_unique_type.data_fields.all()
                  for equipment_unique_type in instance.equipment_unique_types.all()[1:]),
                all=False),
            clear=False)


post_save.connect(
    receiver=equipment_unique_type_group_post_save,
    sender=EquipmentUniqueTypeGroup,
    weak=True,
    dispatch_uid=None)


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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            db_index=True
            # unique=True
        )

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


def equipment_unique_type_post_save(sender, instance, *args, **kwargs):
    for equipment_unique_type_group in instance.groups.all():
        equipment_unique_type_group.save()


post_save.connect(
    receiver=equipment_unique_type_post_save,
    sender=EquipmentUniqueType,
    weak=True,
    dispatch_uid=None)


@python_2_unicode_compatible
class EquipmentFacility(Model):
    RELATED_NAME = 'equipment_facilities'
    RELATED_QUERY_NAME = 'equipment_facility'

    name = \
        CharField(
            verbose_name='Equipment Facility Name',
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    data_file_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_file_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    measure_data_file_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            default=None,
            db_index=True
            # unique=True
        )

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
