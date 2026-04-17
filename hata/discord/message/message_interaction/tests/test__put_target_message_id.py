import vampytest

from ..fields import put_target_message_id


def _iter_options():
    target_message_id = 202410060004
    
    yield 0, False, {}
    yield 0, True, {'target_message_id': None}
    yield target_message_id, False, {'target_message_id': str(target_message_id)}
    yield target_message_id, True, {'target_message_id': str(target_message_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_message_id(target_message_id, defaults):
    """
    Tests whether ``put_target_message_id`` works as intended.
    
    Parameters
    ----------
    target_message_id : `int`
        value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_message_id(target_message_id, {}, defaults)
