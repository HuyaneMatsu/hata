import vampytest

from ..fields import put_id_into


def _iter_options():
    message_id = 202304260001
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield message_id, False, {'id': str(message_id)}
    yield message_id, True, {'id': str(message_id)}


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
