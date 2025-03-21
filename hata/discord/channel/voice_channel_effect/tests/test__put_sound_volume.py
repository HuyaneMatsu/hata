import vampytest

from ..fields import put_sound_volume


def _iter_options():
    yield 0.0, False, {'sound_volume': 0.0}
    yield 0.0, True, {'sound_volume': 0.0}
    yield 1.0, False, {}
    yield 1.0, True, {'sound_volume': 1.0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sound_volume(input_value, defaults):
    """
    Tests whether ``put_sound_volume`` works as intended.
    
    Parameters
    ----------
    input_value : `float`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sound_volume(input_value, {}, defaults)
