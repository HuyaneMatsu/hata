import vampytest

from ..fields import put_channel_id


def _iter_options():
    channel_id = 202308050005
    
    yield 0, False, {'channel_id': None}
    yield 0, True, {'channel_id': None}
    yield channel_id, False, {'channel_id': str(channel_id)}
    yield channel_id, True, {'channel_id': str(channel_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel_id(input_value, defaults):
    """
    Tests whether ``put_channel_id`` works as intended.
    
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
    return put_channel_id(input_value, {}, defaults)
