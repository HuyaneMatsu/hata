import vampytest

from ..fields import validate_type
from ..preinstanced import MessageType


def test__validate_type__0():
    """
    Validates whether ``validate_type`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (MessageType.call, MessageType.call),
        (MessageType.call.value, MessageType.call)
    ):
        output = validate_type(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_type__1():
    """
    Validates whether ``validate_type`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_type(input_value)
