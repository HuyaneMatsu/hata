import vampytest

from ....user import ClientUserBase, User

from ..stage import ScheduledEventEntityMetadataStage

from .test__ScheduledEventEntityMetadataStage__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataStage__copy():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.copy`` works as intended.
    """
    speaker_ids = [202303130012, 202303130013]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    copy = entity_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataStage__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.copy_with`` works as intended.
    
    Case: No fields given.
    """
    speaker_ids = [202303130014, 202303130015]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    copy = entity_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataStage__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_speaker_ids = [202303130016, 202303130017]
    
    new_speaker_ids = [202303130018, 202303130019]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = old_speaker_ids,
    )
    copy = entity_metadata.copy_with(
        speaker_ids = new_speaker_ids,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, entity_metadata)
    vampytest.assert_eq(copy.speaker_ids, tuple(new_speaker_ids))


def test__ScheduledEventEntityMetadataStage__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    speaker_ids = [202303170024, 202303170025]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = speaker_ids,
    )
    copy = entity_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entity_metadata)
    vampytest.assert_is_not(copy, entity_metadata)


def test__ScheduledEventEntityMetadataStage__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataStage.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_speaker_ids = [202303170027, 202303170028]
    
    new_speaker_ids = [202303170029, 202303170030]
    
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = old_speaker_ids,
    )
    copy = entity_metadata.copy_with_keyword_parameters({
        'speaker_ids': new_speaker_ids,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, entity_metadata)
    vampytest.assert_eq(copy.speaker_ids, tuple(new_speaker_ids))


def _iter_options__iter_speaker_ids():
    user_id_0 = 202303130020
    user_id_1 = 202303130021
    
    yield None, []
    yield [user_id_0], [user_id_0]
    yield [user_id_0, user_id_1], [user_id_0, user_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_speaker_ids()).returning_last())
def test__ScheduledEventEntityMetadataStage__iter_speaker_ids(input_value):
    """
    Tests whether ``ScheduledEventEntityMetadataStage.iter_speaker_ids` work as intended.
    
    Parameters
    ----------
    input_value : `None | `list<int>`
        Speaker identifiers to create metadata with.
    
    Returns
    -------
    output : `list<int>`
    """
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = input_value,
    )
    
    output = [*entity_metadata.iter_speaker_ids()]
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output


def _iter_options__speakers():
    user_id_0 = 202303130022
    user_id_1 = 202303130023
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, None
    yield [user_id_0], (user_0, )
    yield [user_id_0, user_id_1], (user_0, user_1)


@vampytest._(vampytest.call_from(_iter_options__speakers()).returning_last())
def test__ScheduledEventEntityMetadataStage__speakers(input_value):
    """
    Tests whether ``ScheduledEventEntityMetadataStage.speakers` work as intended.
    
    Parameters
    ----------
    input_value : `None | `list<int>`
        Speaker identifiers to create metadata with.
    
    Returns
    -------
    output : ``None | tuple<<ClientUserBase>``
    """
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = input_value,
    )
    
    output = entity_metadata.speakers
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
    
    return output


def _iter_options__iter_speakers():
    user_id_0 = 202303130024
    user_id_1 = 202303130025
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, []
    yield [user_id_0], [user_0]
    yield [user_id_0, user_id_1], [user_0, user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_speakers()).returning_last())
def test__ScheduledEventEntityMetadataStage__iter_speakers(input_value):
    """
    Tests whether ``ScheduledEventEntityMetadataStage.iter_speakers` work as intended.
    
    Parameters
    ----------
    input_value : `None | `list<int>`
        Speaker identifiers to create metadata with.
    
    Returns
    -------
    output : ``list<ClientUserBase>``
    """
    entity_metadata = ScheduledEventEntityMetadataStage(
        speaker_ids = input_value,
    )
    
    output = [*entity_metadata.iter_speakers()]
    
    for element in output:
        vampytest.assert_instance(element, ClientUserBase)
    
    return output
