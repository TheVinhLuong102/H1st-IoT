from datetime import date, timedelta
import sys

from h1st.util.date_time import DATE_COL
from h1st.IoT.PredMaint import project


PROJECT, EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP = sys.argv[1:4]


today = date.today()

project(name=PROJECT) \
    .load_equipment_data(
        '{}---{}'.format(EQUIPMENT_GENERAL_TYPE.upper(), EQUIPMENT_UNIQUE_TYPE_GROUP),
        _from_files=True,
        _spark=True,
        set_i_col=True,
        set_t_col=True) \
    .filterByPartitionKeys(
        (DATE_COL,
         today - timedelta(days=1),
         today))
