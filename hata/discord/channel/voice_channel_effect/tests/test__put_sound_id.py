import vampytest

from ..fields import put_sound_id


def _iter_options():
    sound_id = 202408180001
    
    yield 0, False, {}
    yield 0, True, {'sound_id': None}
    yield sound_id, False, {'sound_id': str(sound_id)}
    yield sound_id, True, {'sound_id': str(sound_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sound_id(input_value, defaults):
    """
    Tests whether ``put_sound_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sound_id(input_value, {}, defaults)
