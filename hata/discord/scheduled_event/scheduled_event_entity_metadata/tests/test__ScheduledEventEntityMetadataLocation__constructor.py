import vampytest

from ..location import ScheduledEventEntityMetadataLocation


def _assert_fields_set(entity_metadata):
    """
    Tests whether all attributes of an ``ScheduledEventEntityMetadataLocation`` are set.
    
    Parameters
    ----------
    entity_metadata : ``ScheduledEventEntityMetadataLocation``
        The entity detail to check out.
    """
    vampytest.assert_instance(entity_metadata, ScheduledEventEntityMetadataLocation)
    vampytest.assert_instance(entity_metadata.location, str, nullable = True)
        

def test__ScheduledEventEntityMetadataLocation__new__0():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    entity_metadata = ScheduledEventEntityMetadataLocation(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ScheduledEventEntityMetadataLocation__new__1():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    
    Case: All fields given.
    """
    location = 'Koishi WonderLand'
    
    keyword_parameters = {
        'location': location,
    }
    
    entity_metadata = ScheduledEventEntityMetadataLocation(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(entity_metadata.location, location)


def test__ScheduledEventEntityMetadataLocation__create_empty():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation._create_empty`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation._create_empty()
    _assert_fields_set(entity_metadata)
