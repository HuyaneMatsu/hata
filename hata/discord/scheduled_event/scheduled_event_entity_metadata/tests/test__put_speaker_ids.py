import vampytest

from ..fields import put_speaker_ids


def _iter_options():
    user_id_0 = 202506230000
    user_id_1 = 202506230001
    
    yield None, False, {}
    yield None, True, {'speaker_ids': []}
    yield (user_id_0, user_id_1,), False, {'speaker_ids': [str(user_id_0), str(user_id_1)]}
    yield (user_id_0, user_id_1,), True, {'speaker_ids': [str(user_id_0), str(user_id_1)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_speaker_ids(input_value, defaults):
    """
    Tests whether ``put_speaker_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Value to serialize.
    
    defaults : `bool`
        Whether values as their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_speaker_ids(input_value, {}, defaults)
