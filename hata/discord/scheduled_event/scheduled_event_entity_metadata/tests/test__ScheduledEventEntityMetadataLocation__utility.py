import vampytest

from ..location import ScheduledEventEntityMetadataLocation

from .test__ScheduledEventEntityMetadataLocation__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataLocation__copy():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.copy`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    copy = entity_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataLocation__copy_with__0():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.copy_with`` works as intended.
    
    Case: No fields given.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    copy = entity_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataLocation__copy_with__1():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_location = 'Koishi WonderLand'
    
    new_location = 'Orin\'s dance house'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = old_location,
    )
    copy = entity_metadata.copy_with(
        location = new_location,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, entity_metadata)
    vampytest.assert_eq(copy.location, new_location)


def test__ScheduledEventEntityMetadataLocation__copy_with_keyword_parameters__0():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    copy = entity_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataLocation__copy_with_keyword_parameters__1():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_location = 'Koishi WonderLand'
    
    new_location = 'Orin\'s dance house'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = old_location,
    )
    copy = entity_metadata.copy_with_keyword_parameters({
        'location': new_location,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, entity_metadata)
    vampytest.assert_eq(copy.location, new_location)
