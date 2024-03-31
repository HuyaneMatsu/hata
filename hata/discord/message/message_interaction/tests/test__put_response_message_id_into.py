import vampytest

from ..fields import put_response_message_id_into


def _iter_options():
    response_message_id = 202403250003
    
    yield 0, False, {}
    yield 0, True, {'original_response_message_id': None}
    yield response_message_id, False, {'original_response_message_id': str(response_message_id)}
    yield response_message_id, True, {'original_response_message_id': str(response_message_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_response_message_id_into(response_message_id, defaults):
    """
    Tests whether ``put_response_message_id_into`` works as intended.
    
    Parameters
    ----------
    response_message_id : `int`
        value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_response_message_id_into(response_message_id, {}, defaults)
