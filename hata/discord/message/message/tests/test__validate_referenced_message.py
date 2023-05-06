import vampytest

from ..fields import validate_referenced_message
from ..message import Message


def test__validate_referenced_message__0():
    """
    Tests whether ``validate_referenced_message`` works as intended.
    
    Case: Passing.
    """
    message = Message.precreate(202305010035)
    
    for input_value, expected_output in (
        (None, None),
        (message, message),
    ):
        output = validate_referenced_message(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_referenced_message__1():
    """
    Tests whether ``validate_referenced_message`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_referenced_message(input_value)
