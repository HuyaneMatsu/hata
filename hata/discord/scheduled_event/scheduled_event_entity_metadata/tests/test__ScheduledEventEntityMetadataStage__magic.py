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


def _iter_options__eq():
    speaker_ids = [202303130008, 202303130009]
    
    keyword_parameters = {
        'speaker_ids': speaker_ids,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'speaker_ids': None,
        },
        False,
    )



@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventEntityMetadataStage__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    entity_metadata_0 = ScheduledEventEntityMetadataStage(**keyword_parameters_0)
    entity_metadata_1 = ScheduledEventEntityMetadataStage(**keyword_parameters_1)
    
    output = entity_metadata_0 == entity_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventEntityMetadataStage__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.__hash__`` works as intended.
    """
    speaker_ids = [202303130010, 202303130011]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    
    vampytest.assert_instance(hash(entity_metadata), int)
