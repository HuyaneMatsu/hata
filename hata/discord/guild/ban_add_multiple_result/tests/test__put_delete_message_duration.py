import vampytest

from ..constants import DELETE_MESSAGE_DURATION_DEFAULT
from ..fields import put_delete_message_duration


def _iter_options():
    yield DELETE_MESSAGE_DURATION_DEFAULT, False, {}
    yield DELETE_MESSAGE_DURATION_DEFAULT, True, {'delete_message_seconds': DELETE_MESSAGE_DURATION_DEFAULT}
    yield 60, False, {'delete_message_seconds': 60}
    yield 60, True, {'delete_message_seconds': 60}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_delete_message_duration(input_value, defaults):
    """
    Tests whether ``put_delete_message_duration`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_delete_message_duration(input_value, {}, defaults)
