from django.db.models import \
    Model, \
    BooleanField, CharField, FloatField, ForeignKey, ManyToManyField, URLField, \
    CASCADE, PROTECT, SET_NULL

from arimo.IoT.DataAdmin.util import clean_lower_str


_MAX_CHAR_LEN = 255


class DataType(Model):
    name = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    class Meta:
        ordering = 'name',

    def __unicode__(self):
        return 'Data Type "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(DataType, self).save(*args, **kwargs)


class EquipmentDataFieldType(Model):
    name = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    class Meta:
        ordering = 'name',

    def __unicode__(self):
        return 'Equipment Data Field Type "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentDataFieldType, self).save(*args, **kwargs)


class EquipmentGeneralType(Model):
    name = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    class Meta:
        ordering = 'name',

    def __unicode__(self):
        return 'Equipment General Type "{}"'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentGeneralType, self).save(*args, **kwargs)


class EquipmentDataField(Model):
    RELATED_NAME = 'equipment_data_fields'
    RELATED_QUERY_NAME = 'equipment_data_field'

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
            max_length=_MAX_CHAR_LEN,
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
            blank=True,
            null=True)

    upper_numeric_null = \
        FloatField(
            blank=True,
            null=True)

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

    def __unicode__(self):
        return '{} [{}] {} [{}]'.format(
            self.equipment_general_type.name.upper(),
            self.equipment_data_field_type.name,
            self.name,
            self.data_type.name
                if self.data_type
                else 'UNTYPED')

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentDataField, self).save(*args, **kwargs)


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
            max_length=_MAX_CHAR_LEN,
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

    class Meta:
        ordering = 'equipment_general_type', 'name'

    def __unicode__(self):
        return '{} Unique Type {}'.format(
            self.equipment_general_type.name.upper(),
            self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentUniqueType, self).save(*args, **kwargs)


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
            max_length=_MAX_CHAR_LEN,
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
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    data_db_tbl = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    data_file_url = \
        URLField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_db_url = \
        URLField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_db_tbl = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    control_data_file_url = \
        URLField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    measure_data_db_url = \
        URLField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    measure_data_db_tbl = \
        CharField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    measure_data_file_url = \
        URLField(
            max_length=_MAX_CHAR_LEN,
            blank=True,
            null=True,
            default=None)

    class Meta:
        ordering = 'equipment_general_type', 'equipment_unique_type', 'name'

    def __unicode__(self):
        return '{} Instance "{}"'.format(
            self.equipment_unique_type
            if self.equipment_unique_type
            else self.equipment_general_type,
            self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentInstance, self).save(*args, **kwargs)
