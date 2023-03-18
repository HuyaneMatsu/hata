import vampytest

from ..stage import ScheduledEventEntityMetadataStage

from .test__ScheduledEventEntityMetadataStage__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataStage__from_data__0():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.from_data`` works as intended.
    
    Case: non-discord entity.
    """
    speaker_ids = [202303130002, 202303130003]
    
    data = {
        'speaker_ids': [str(speaker_id) for speaker_id in speaker_ids],
    }
    
    entity_metadata = ScheduledEventEntityMetadataStage.from_data(data)
    
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(entity_metadata.speaker_ids, tuple(speaker_ids))


def test__ScheduledEventEntityMetadataStage__to_data():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.to_data`` works as intended.
    
    Case: defaults.
    """
    speaker_ids = [202303130004, 202303130005]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    
    expected_data = {
        'speaker_ids': [str(speaker_id) for speaker_id in speaker_ids],
    }
    
    vampytest.assert_eq(
        entity_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
