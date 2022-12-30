import vampytest

from ...activity_metadata import ActivityMetadataBase

from ..preinstanced import ActivityType


def test__ActivityType__name():
    """
    Tests whether ``ActivityType`` instance names are all strings.
    """
    for instance in ActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ActivityType__value():
    """
    Tests whether ``ActivityType`` instance values are all the expected value type.
    """
    for instance in ActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ActivityType.VALUE_TYPE)
    
    
def test__ActivityType__metadata_type():
    """
    Tests whether ``ActivityType`` instance metadata types are all metadata types.
    """
    for instance in ActivityType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, ActivityMetadataBase)
