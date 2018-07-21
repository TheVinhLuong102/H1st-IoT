from django.db.models import \
    Model, \
    BooleanField, CharField, DateField, FloatField, ForeignKey, ManyToManyField, URLField, \
    CASCADE, PROTECT, SET_NULL
from django.utils.encoding import python_2_unicode_compatible

from ..util import MAX_CHAR_LEN, clean_lower_str


@python_2_unicode_compatible
class DataType(Model):
    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'DataTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(DataType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentDataFieldType(Model):
    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

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

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False)

    data_type = \
        ForeignKey(
            to=DataType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    nullable = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

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

    class Meta:
        ordering = 'equipment_general_type', 'equipment_data_field_type', 'name'

    def __str__(self):
        return '{} [{}] {} [{}{}{}{}{}]'.format(
            self.equipment_general_type.name.upper(),
            self.equipment_data_field_type.name,
            self.name,
            self.data_type.name
                if self.data_type
                else 'UNTYPED',
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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False)

    equipment_unique_types = \
        ManyToManyField(
            to='EquipmentUniqueType',
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        ordering = 'equipment_general_type', 'name'

    def __str__(self):
        return 'EqUnqTpGrp {}'.format(
            # self.equipment_general_type.name.upper(),   # *** THIS WILL MAKE ADMIN VIEWS BUTCHER THE DATABASE ***
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
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False)

    # *** USING 'equipment_data_fields' (corresponding to EquipmentDataField above) LEADS TO BUG ***
    data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            through=EquipmentDataField.equipment_unique_types.through,
            # related_name=RELATED_NAME,
            # related_query_name=RELATED_QUERY_NAME,
            blank=True)

    # *** USING 'equipment_unique_type_groups' (corresponding to EquipmentUniqueTypeGroup above) LEADS TO BUG ***
    groups = \
        ManyToManyField(
            to=EquipmentUniqueTypeGroup,
            through=EquipmentUniqueTypeGroup.equipment_unique_types.through,
            # related_name=RELATED_NAME,
            # related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        ordering = 'equipment_general_type', 'name'

    def __str__(self):
        return 'EqUnqTp {}'.format(
            # self.equipment_general_type.name.upper(),   # *** THIS WILL MAKE ADMIN VIEWS BUTCHER THE DATABASE ***
            self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentUniqueType, self).save(*args, **kwargs)


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

    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False)

    data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    data_db_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    data_db_tbl = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    data_file_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_db_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_db_tbl = \
        CharField(
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

    measure_data_db_url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    measure_data_db_tbl = \
        CharField(
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
        ordering = 'equipment_general_type', 'equipment_unique_type', 'name'

    def __str__(self):
        return 'EqInst #{}'.format(
                # self.equipment_unique_type
                #     if self.equipment_unique_type
                #     else self.equipment_general_type,   # *** THIS CAN MAKE ADMIN VIEWS BUTCHER THE DATABASE ***
                self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentInstance, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentInstanceAssociation(Model):
    RELATED_NAME = 'equipment_instance_associations'
    RELATED_QUERY_NAME = 'equipment_instance_association'

    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            default=None)

    date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_now_add=False)

    equipment_instances = \
        ManyToManyField(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        ordering = 'name', 'date'

    def __str__(self):
        return '{} on {}'.format(self.name, self.date)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentInstanceAssociation, self).save(*args, **kwargs)
