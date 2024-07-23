import vampytest

from ...message import Message

from ..request_helpers import get_message_id


def _iter_options__passing():
    message_id = 202407220000
    
    yield message_id, message_id
    yield Message.precreate(message_id), message_id


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_message_id(input_value):
    """
    tests whether ``get_message_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    """
    output = get_message_id(input_value)
    vampytest.assert_instance(output, int)
    return output
