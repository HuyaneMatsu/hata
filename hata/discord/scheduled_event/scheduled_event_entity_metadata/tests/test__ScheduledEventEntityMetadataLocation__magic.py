import vampytest

from ..location import ScheduledEventEntityMetadataLocation


def test__ScheduledEventEntityMetadataLocation__repr():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    
    vampytest.assert_instance(repr(entity_metadata), str)


def test__ScheduledEventEntityMetadataLocation__eq():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__eq__`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    keyword_parameters = {
        'location': location,
    }
    
    entity_metadata = ScheduledEventEntityMetadataLocation(**keyword_parameters)
    
    vampytest.assert_eq(entity_metadata, entity_metadata)
    vampytest.assert_ne(entity_metadata, object())
    
    for field_name, field_value in (
        ('location', 'Orin\'s dance house'),
    ):
        entity_metadata_test = ScheduledEventEntityMetadataLocation(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(entity_metadata, entity_metadata_test)


def test__ScheduledEventEntityMetadataLocation__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__hash__`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
       location = location,
    )
    
    vampytest.assert_instance(hash(entity_metadata), int)
