import vampytest

from ..fields import put_interacted_message_id_into


def _iter_options():
    interacted_message_id = 202403250018
    
    yield 0, False, {}
    yield 0, True, {'interacted_message_id': None}
    yield interacted_message_id, False, {'interacted_message_id': str(interacted_message_id)}
    yield interacted_message_id, True, {'interacted_message_id': str(interacted_message_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_interacted_message_id_into(interacted_message_id, defaults):
    """
    Tests whether ``put_interacted_message_id_into`` works as intended.
    
    Parameters
    ----------
    interacted_message_id : `int`
        value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_interacted_message_id_into(interacted_message_id, {}, defaults)
