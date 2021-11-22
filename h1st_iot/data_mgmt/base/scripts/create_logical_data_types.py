"""Create CAT & NUM logical data types."""


from h1st_iot.data_mgmt.base.models import LogicalDataType


def run():
    """Run this script to create CAT & NUM logical data types."""
    print(LogicalDataType.objects.get_or_create(name='cat')[0])
    print(LogicalDataType.objects.get_or_create(name='num')[0])
