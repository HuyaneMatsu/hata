import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..preinstanced import ScheduledEventEntityType


def test__ScheduledEventEntityType__name():
    """
    Tests whether ``ScheduledEventEntityType`` instance names are all strings.
    """
    for instance in ScheduledEventEntityType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ScheduledEventEntityType__value():
    """
    Tests whether ``ScheduledEventEntityType`` instance values are all the expected value type.
    """
    for instance in ScheduledEventEntityType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ScheduledEventEntityType.VALUE_TYPE)


def test__ScheduledEventEntityType__metadata_type():
    """
    Tests whether ``ScheduledEventEntityType`` instance metadata_types are all the expected metadata_type type.
    """
    for instance in ScheduledEventEntityType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, ScheduledEventEntityMetadataBase)
