import vampytest

from ..fields import put_id_into


def _iter_options():
    sound_id = 202305240004
    
    yield 0, False, {'sound_id': None}
    yield 0, True, {'sound_id': None}
    yield sound_id, False, {'sound_id': str(sound_id)}
    yield sound_id, True, {'sound_id': str(sound_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id_into(input_value, defaults):
    """
    Tests whether ``put_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_id_into(input_value, {}, defaults)
