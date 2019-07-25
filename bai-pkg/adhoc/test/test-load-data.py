import sys

from arimo.IoT.PredMaint import project


PROJECT, EQUIPMENT_GENERAL_TYPE, EQUIPMENT_UNIQUE_TYPE_GROUP = sys.argv[1:4]


project(name=PROJECT) \
    .load_equipment_data(
        '{}---{}'.format(EQUIPMENT_GENERAL_TYPE.upper(), EQUIPMENT_UNIQUE_TYPE_GROUP),
        _from_files=True,
        _spark=True,
        set_i_col=True,
        set_t_col=True)
