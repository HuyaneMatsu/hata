import vampytest

from ..fields import put_id


def _iter_options():
    emoji_id = 202212310002
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield emoji_id, False, {'id': str(emoji_id)}
    yield emoji_id, True, {'id': str(emoji_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id(input_value, defaults):
    """
    Tests whether ``put_id`` works as intended.
    
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
    return put_id(input_value, {}, defaults)
