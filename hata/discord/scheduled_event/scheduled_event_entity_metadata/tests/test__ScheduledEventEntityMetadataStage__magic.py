import vampytest

from ..stage import ScheduledEventEntityMetadataStage


def test__ScheduledEventEntityMetadataStage__repr():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__new__`` works as intended.
    """
    speaker_ids = [202303130006, 202303130007]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    
    vampytest.assert_instance(repr(entity_metadata), str)


def test__ScheduledEventEntityMetadataStage__eq():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__eq__`` works as intended.
    """
    speaker_ids = [202303130008, 202303130009]
    
    keyword_parameters = {
        'speaker_ids': speaker_ids,
    }
    
    entity_metadata = ScheduledEventEntityMetadataStage(**keyword_parameters)
    
    vampytest.assert_eq(entity_metadata, entity_metadata)
    vampytest.assert_ne(entity_metadata, object())
    
    for field_name, field_value in (
        ('speaker_ids', None),
    ):
        entity_metadata_test = ScheduledEventEntityMetadataStage(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(entity_metadata, entity_metadata_test)


def test__ScheduledEventEntityMetadataStage__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__hash__`` works as intended.
    """
    speaker_ids = [202303130010, 202303130011]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    
    vampytest.assert_instance(hash(entity_metadata), int)
