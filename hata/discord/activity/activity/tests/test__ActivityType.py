import vampytest

from ...activity_metadata import ActivityMetadataBase

from ..preinstanced import ActivityType


@vampytest.call_from(ActivityType.INSTANCES.values())
def test__ActivityType__instances(instance):
    """
    Tests whether ``ActivityType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ActivityType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ActivityType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ActivityType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, ActivityMetadataBase)
