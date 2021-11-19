from typing import Optional


def run(equipment_general_type_name: str,
        equipment_unique_type_group_name: str,
        to_month: Optional[str] = None):
    equipment_unique_type_group_data_set_name = \
        '{}---{}'.format(
            equipment_general_type_name.upper(),
            equipment_unique_type_group_name)

    equipment_unique_type_group_s3_parquet_df = \
        self.load_equipment_data(
            equipment_unique_type_group_data_set_name,
            spark=False, set_i_col=True, set_t_col=False,
            verbose=True)

    if to_month:
        to_date = month_end(to_month)

        equipment_unique_type_group_s3_parquet_df = \
            equipment_unique_type_group_s3_parquet_df.filterByPartitionKeys(
                (DATE_COL,
                    str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                        relativedelta(months=self.REF_N_MONTHS - 1)).date()),
                    str(to_date)))

    else:
        to_date = None

    equipment_unique_type_group = \
        self.data.EquipmentUniqueTypeGroups.get(
            equipment_general_type__name=equipment_general_type_name,
            name=equipment_unique_type_group_name)

    self.data.EquipmentUniqueTypeGroupDataFieldProfiles.filter(
        equipment_unique_type_group=equipment_unique_type_group,
        to_date=to_date) \
    .delete()

    for equipment_data_field in tqdm(equipment_unique_type_group.equipment_data_fields.all()):
        equipment_data_field_name = equipment_data_field.name

        if equipment_data_field_name in equipment_unique_type_group_s3_parquet_df.possibleFeatureContentCols:
            if equipment_unique_type_group_s3_parquet_df.typeIsNum(equipment_data_field_name):
                equipment_unique_type_group_s3_parquet_df._nulls[equipment_data_field_name] = \
                    equipment_data_field.lower_numeric_null, \
                    equipment_data_field.upper_numeric_null

            _distinct_values_proportions = \
                equipment_unique_type_group_s3_parquet_df.distinct(equipment_data_field_name).to_dict()
            _n_distinct_values = len(_distinct_values_proportions)

            equipment_unique_type_group_data_field_profile = \
                self.data.EquipmentUniqueTypeGroupDataFieldProfiles.create(
                    equipment_unique_type_group=equipment_unique_type_group,
                    equipment_data_field=equipment_data_field,
                    to_date=to_date,
                    valid_proportion=
                        equipment_unique_type_group_s3_parquet_df.nonNullProportion(equipment_data_field_name),
                    n_distinct_values=_n_distinct_values)

            if _n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                equipment_unique_type_group_data_field_profile.distinct_values = _distinct_values_proportions

            if equipment_unique_type_group_s3_parquet_df.typeIsNum(equipment_data_field_name):
                quartiles = \
                    equipment_unique_type_group_s3_parquet_df.reprSample[equipment_data_field_name] \
                    .describe(
                        percentiles=(.25, .5, .75)) \
                    .drop(
                        index='count',
                        level=None,
                        inplace=False,
                        errors='raise') \
                    .to_dict()

                equipment_unique_type_group_data_field_profile.sample_min = quartiles['min']
                equipment_unique_type_group_data_field_profile.outlier_rst_min = \
                    equipment_unique_type_group_s3_parquet_df.outlierRstMin(equipment_data_field_name)
                equipment_unique_type_group_data_field_profile.sample_quartile = quartiles['25%']
                equipment_unique_type_group_data_field_profile.sample_median = quartiles['50%']
                equipment_unique_type_group_data_field_profile.sample_3rd_quartile = quartiles['75%']
                equipment_unique_type_group_data_field_profile.outlier_rst_max = \
                    equipment_unique_type_group_s3_parquet_df.outlierRstMax(equipment_data_field_name)
                equipment_unique_type_group_data_field_profile.sample_max = quartiles['max']

            equipment_unique_type_group_data_field_profile.save()

