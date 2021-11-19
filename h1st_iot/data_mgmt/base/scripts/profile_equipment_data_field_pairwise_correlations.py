


def run(equipment_general_type_name: str,
        equipment_unique_type_group_name: str):
    equipment_unique_type_group_data_set_name = \
        '{}---{}'.format(
            equipment_general_type_name.upper(),
            equipment_unique_type_group_name)

    equipment_unique_type_group_s3_parquet_df = \
        self.load_equipment_data(
            equipment_unique_type_group_data_set_name,
            spark=False, set_i_col=True, set_t_col=False,
            verbose=True)

    equipment_unique_type_group = \
        self.data.EquipmentUniqueTypeGroups.get(
            equipment_general_type__name=equipment_general_type_name,
            name=equipment_unique_type_group_name)

    self.data.EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations.filter(
        equipment_unique_type_group=equipment_unique_type_group) \
    .delete()

    equipment_data_fields = equipment_unique_type_group.equipment_data_fields.filter(data_type=self.NUM_DATA_TYPE)

    n_equipment_data_fields = equipment_data_fields.count()

    from h1st_iot.data_mgmt.maint_ops.models import EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation

    for i in tqdm(range(n_equipment_data_fields - 1)):
        equipment_data_field = equipment_data_fields[i]
        equipment_data_field_name = equipment_data_field.name

        if equipment_data_field_name in equipment_unique_type_group_s3_parquet_df.possibleNumContentCols:
            equipment_unique_type_group_s3_parquet_df._nulls[equipment_data_field_name] = \
                equipment_data_field.lower_numeric_null, \
                equipment_data_field.upper_numeric_null

            outlier_rst_min = equipment_unique_type_group_s3_parquet_df.outlierRstMin(equipment_data_field_name)
            outlier_rst_max = equipment_unique_type_group_s3_parquet_df.outlierRstMax(equipment_data_field_name)

            if outlier_rst_min < outlier_rst_max:
                for i_2 in tqdm(range(i + 1, n_equipment_data_fields)):
                    equipment_data_field_2 = equipment_data_fields[i_2]
                    equipment_data_field_name_2 = equipment_data_field_2.name

                    if (equipment_data_field_name_2 != equipment_data_field_name) and \
                            (equipment_data_field_name_2 in equipment_unique_type_group_s3_parquet_df.possibleNumContentCols):
                        equipment_unique_type_group_s3_parquet_df._nulls[equipment_data_field_name_2] = \
                            equipment_data_field_2.lower_numeric_null, \
                            equipment_data_field_2.upper_numeric_null

                        outlier_rst_min_2 = equipment_unique_type_group_s3_parquet_df.outlierRstMin(equipment_data_field_name_2)
                        outlier_rst_max_2 = equipment_unique_type_group_s3_parquet_df.outlierRstMax(equipment_data_field_name_2)

                        if outlier_rst_min_2 < outlier_rst_max_2:
                            sample_df = \
                                equipment_unique_type_group_s3_parquet_df.reprSample.loc[
                                    equipment_unique_type_group_s3_parquet_df.reprSample[equipment_data_field_name].between(
                                        outlier_rst_min,
                                        outlier_rst_max,
                                        inclusive=False) &
                                    equipment_unique_type_group_s3_parquet_df.reprSample[equipment_data_field_name_2].between(
                                        outlier_rst_min_2,
                                        outlier_rst_max_2,
                                        inclusive=False),
                                    [equipment_data_field_name, equipment_data_field_name_2]]

                            if len(sample_df) > 1000:
                                outlier_rst_min = float(sample_df[equipment_data_field_name].min())
                                outlier_rst_max = float(sample_df[equipment_data_field_name].max())

                                if outlier_rst_min < outlier_rst_max:
                                    outlier_rst_min_2 = float(sample_df[equipment_data_field_name_2].min())
                                    outlier_rst_max_2 = float(sample_df[equipment_data_field_name_2].max())

                                    if outlier_rst_min_2 < outlier_rst_max_2:
                                        sample_correlation = \
                                            pearsonr(
                                                x=sample_df[equipment_data_field_name],
                                                y=sample_df[equipment_data_field_name_2])[0]

                                        if pandas.notnull(sample_correlation):
                                            self.data.EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations.bulk_create(
                                                [EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(
                                                    equipment_unique_type_group=equipment_unique_type_group,
                                                    equipment_data_field=equipment_data_field,
                                                    equipment_data_field_2=equipment_data_field_2,
                                                    sample_correlation=sample_correlation),
                                                    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(
                                                    equipment_unique_type_group=equipment_unique_type_group,
                                                    equipment_data_field=equipment_data_field_2,
                                                    equipment_data_field_2=equipment_data_field,
                                                    sample_correlation=sample_correlation)])
