import vampytest

from ....message import Message

from ..fields import validate_message


def test__validate_message__0():
    """
    Tests whether ``validate_message`` works as intended.
    
    Case: Passing.
    """
    message_id = 202210280007
    channel_id = 202210280014
    message = Message.precreate(message_id, channel_id = channel_id)
    
    
    for input_value in (
        None,
        message,
    ):
        validate_message(input_value)


def test__validate_message__1():
    """
    Tests whether ``validate_message`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_message(input_value)
