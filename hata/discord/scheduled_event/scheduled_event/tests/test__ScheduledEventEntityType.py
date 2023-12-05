import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..preinstanced import ScheduledEventEntityType


@vampytest.call_from(ScheduledEventEntityType.INSTANCES.values())
def test__ScheduledEventEntityType__instances(instance):
    """
    Tests whether ``ScheduledEventEntityType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduledEventEntityType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ScheduledEventEntityType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ScheduledEventEntityType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, ScheduledEventEntityMetadataBase)
