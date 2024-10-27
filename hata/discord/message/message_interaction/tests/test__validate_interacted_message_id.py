import vampytest

from ...message import Message

from ..fields import validate_interacted_message_id


def _iter_options__passing():
    interacted_message_id = 202403250053
    message = Message.precreate(interacted_message_id, content = 'blossom')
    yield interacted_message_id, interacted_message_id
    yield message, interacted_message_id
    yield None, 0


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_interacted_message_id__passing(input_value):
    """
    Tests whether `validate_interacted_message_id` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    output = validate_interacted_message_id(input_value)
    vampytest.assert_instance(output, int)
    return output
