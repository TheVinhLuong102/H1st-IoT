import datetime
import sys

from arimo.util.date_time import DATE_COL, month_str
from arimo.IoT.PredMaint import project


PROJECT, EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP = sys.argv[1:4]


mth_str = month_str(str(datetime.date.today()), n_months_offset=-1)

project(name=PROJECT) \
    .load_equipment_data(
        '{}---{}'.format(EQUIPMENT_GENERAL_TYPE.upper(), EQUIPMENT_UNIQUE_TYPE_GROUP),
        _from_files=True,
        _spark=True,
        set_i_col=True,
        set_t_col=True) \
    .filterByPartitionKeys(
        (DATE_COL,
         mth_str + '-01',
         mth_str + '-31'))
