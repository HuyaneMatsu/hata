import vampytest

from ..constants import CUSTOM_MESSAGE_LENGTH_MAX
from ..fields import validate_custom_message


def test__validate_custom_message__0():
    """
    Tests whether `validate_custom_message` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_custom_message(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_custom_message__1():
    """
    Tests whether `validate_custom_message` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_custom_message(input_value)


def test__validate_custom_message__2():
    """
    Tests whether `validate_custom_message` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (CUSTOM_MESSAGE_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_custom_message(input_value)
