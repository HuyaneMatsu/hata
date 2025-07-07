import vampytest

from ..base import ScheduledEventEntityMetadataBase

from .test__ScheduledEventEntityMetadataBase__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataBase__copy():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.copy`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    copy = entity_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataBase__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    copy = entity_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataBase__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    copy = entity_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataBase__placeholders():
    """
    Tests whether ``ScheduledEventEntityMetadataBase``'s placeholders work as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    vampytest.assert_instance(entity_metadata.location, str, nullable = True)
    vampytest.assert_instance(entity_metadata.speaker_ids, tuple, nullable = True)


def test__ScheduledEventEntityMetadataBase__iter_speaker_ids():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.iter_speaker_ids` work as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    vampytest.assert_eq([*entity_metadata.iter_speaker_ids()], [])


def test__ScheduledEventEntityMetadataBase__speakers():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.iter_speaker_ids` work as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    vampytest.assert_eq(entity_metadata.speakers, None)


def test__ScheduledEventEntityMetadataBase__iter_speakers():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.iter_speakers` work as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    vampytest.assert_eq([*entity_metadata.iter_speakers()], [])
