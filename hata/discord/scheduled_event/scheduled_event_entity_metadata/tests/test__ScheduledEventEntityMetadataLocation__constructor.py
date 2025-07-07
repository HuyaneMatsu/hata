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
        

def test__ScheduledEventEntityMetadataLocation__new__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    
    Case: No fields given.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation()
    _assert_fields_set(entity_metadata)


def test__ScheduledEventEntityMetadataLocation__new__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    
    Case: All fields given.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(location = location)
    _assert_fields_set(entity_metadata)
    
    vampytest.assert_eq(entity_metadata.location, location)


def test__ScheduledEventEntityMetadataLocation__from_keyword_parameters__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    entity_metadata = ScheduledEventEntityMetadataLocation.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ScheduledEventEntityMetadataLocation__from_keyword_parameters__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    location = 'Koishi WonderLand'
    
    keyword_parameters = {
        'location': location,
    }
    
    entity_metadata = ScheduledEventEntityMetadataLocation.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(entity_metadata.location, location)


def test__ScheduledEventEntityMetadataLocation__create_empty():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation._create_empty`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation._create_empty()
    _assert_fields_set(entity_metadata)

