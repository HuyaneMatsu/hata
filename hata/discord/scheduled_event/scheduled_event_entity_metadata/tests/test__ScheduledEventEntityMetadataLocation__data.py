import vampytest

from ..location import ScheduledEventEntityMetadataLocation

from .test__ScheduledEventEntityMetadataLocation__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataLocation__from_data__0():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.from_data`` works as intended.
    
    Case: non-discord entity.
    """
    location = 'Koishi WonderLand'
    
    data = {
        'location': location,
    }
    
    entity_metadata = ScheduledEventEntityMetadataLocation.from_data(data)
    
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(entity_metadata.location, location)


def test__ScheduledEventEntityMetadataLocation__to_data():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.to_data`` works as intended.
    
    Case: defaults.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    
    expected_data = {
        'location': location,
    }
    
    vampytest.assert_eq(
        entity_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
