import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..preinstanced import ScheduledEventEntityType


def _assert_fields_set(scheduled_event_entity_type):
    """
    Asserts whether every field are set of the given scheduled event entity type.
    
    Parameters
    ----------
    scheduled_event_entity_type : ``ScheduledEventEntityType``
        The instance to test.
    """
    vampytest.assert_instance(scheduled_event_entity_type, ScheduledEventEntityType)
    vampytest.assert_instance(scheduled_event_entity_type.name, str)
    vampytest.assert_instance(scheduled_event_entity_type.value, ScheduledEventEntityType.VALUE_TYPE)
    vampytest.assert_subtype(scheduled_event_entity_type.metadata_type, ScheduledEventEntityMetadataBase)


@vampytest.call_from(ScheduledEventEntityType.INSTANCES.values())
def test__ScheduledEventEntityType__instances(instance):
    """
    Tests whether ``ScheduledEventEntityType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduledEventEntityType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ScheduledEventEntityType__new__min_fields():
    """
    Tests whether ``ScheduledEventEntityType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ScheduledEventEntityType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ScheduledEventEntityType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, ScheduledEventEntityMetadataBase)
        vampytest.assert_is(ScheduledEventEntityType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ScheduledEventEntityType.INSTANCES[value]
        except KeyError:
            pass
