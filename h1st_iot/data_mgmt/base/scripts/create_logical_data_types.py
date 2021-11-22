"""Create CAT & NUM logical data types."""


from h1st_iot.data_mgmt.base.models import DataType


def run():
    """Run this script to create CAT & NUM logical data types."""
    print(DataType.objects.get_or_create(name='cat')[0])
    print(DataType.objects.get_or_create(name='num')[0])
