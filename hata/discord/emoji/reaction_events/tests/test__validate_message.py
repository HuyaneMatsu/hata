import vampytest

from ....message import Message

from ..fields import validate_message


def test__validate_message__0():
    """
    Tests whether ``validate_message`` works as intended.
    
    Case: Passing.
    """
    message = Message.precreate(202301020024)
    
    for input_value, expected_output in (
        (message, message),
    ):
        output = validate_message(input_value)
        vampytest.assert_eq(output, expected_output)


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
