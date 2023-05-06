import vampytest

from ..fields import validate_flags
from ..flags import MessageFlag


def test__validate_flags__0():
    """
    Tests whether `validate_flags` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, MessageFlag(1)),
        (MessageFlag(1), MessageFlag(1)),
    ):
        output = validate_flags(input_value)
        vampytest.assert_instance(output, MessageFlag)
        vampytest.assert_eq(output, expected_output)


def test__validate_flags__1():
    """
    Tests whether `validate_flags` works as intended.
    
    Case: type error
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_flags(input_value)
