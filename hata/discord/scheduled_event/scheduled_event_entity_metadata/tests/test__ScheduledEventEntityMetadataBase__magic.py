import vampytest

from ..base import ScheduledEventEntityMetadataBase


def test__ScheduledEventEntityMetadataBase__repr():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__new__`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase({})
    
    vampytest.assert_instance(repr(entity_metadata), str)


def test__ScheduledEventEntityMetadataBase__eq():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    entity_metadata = ScheduledEventEntityMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(entity_metadata, entity_metadata)
    vampytest.assert_ne(entity_metadata, object())
    
    for field_name, field_value in ():
        entity_metadata_test = ScheduledEventEntityMetadataBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(entity_metadata, entity_metadata_test)


def test__ScheduledEventEntityMetadataBase__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__hash__`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase({})
    
    vampytest.assert_instance(hash(entity_metadata), int)
