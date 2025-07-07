import vampytest

from ..stage import ScheduledEventEntityMetadataStage


def _assert_fields_set(entity_metadata):
    """
    Tests whether all attributes of an ``ScheduledEventEntityMetadataStage`` are set.
    
    Parameters
    ----------
    entity_metadata : ``ScheduledEventEntityMetadataStage``
        The entity detail to check out.
    """
    vampytest.assert_instance(entity_metadata, ScheduledEventEntityMetadataStage)
    vampytest.assert_instance(entity_metadata.speaker_ids, tuple, nullable = True)
        

def test__ScheduledEventEntityMetadataStage__new__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__new__`` works as intended.
    
    Case: No fields given.
    """
    entity_metadata = ScheduledEventEntityMetadataStage()
    _assert_fields_set(entity_metadata)


def test__ScheduledEventEntityMetadataStage__new__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__new__`` works as intended.
    
    Case: All fields given.
    """
    speaker_ids = [202303130000, 202303130001]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    _assert_fields_set(entity_metadata)
    
    vampytest.assert_eq(entity_metadata.speaker_ids, tuple(speaker_ids))


def test__ScheduledEventEntityMetadataStage__from_keyword_parameters__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    entity_metadata = ScheduledEventEntityMetadataStage.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ScheduledEventEntityMetadataStage__from_keyword_parameters__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    speaker_ids = [202303170022, 202303170023]
    
    keyword_parameters = {
        'speaker_ids': speaker_ids,
    }
    
    entity_metadata = ScheduledEventEntityMetadataStage.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(entity_metadata.speaker_ids, tuple(speaker_ids))


def test__ScheduledEventEntityMetadataStage__create_empty():
    """
    Tests whether ``ScheduledEventEntityMetadataStage._create_empty`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataStage._create_empty()
    _assert_fields_set(entity_metadata)
