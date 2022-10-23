import vampytest

from ..constants import PLACEHOLDER_LENGTH_MAX
from ..fields import validate_placeholder


def test__validate_placeholder__0():
    """
    Tests whether `validate_placeholder` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('a', 'a'),
    ):
        output = validate_placeholder(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_placeholder__1():
    """
    Tests whether `validate_placeholder` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (PLACEHOLDER_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_placeholder(input_value)


def test__validate_placeholder__2():
    """
    Tests whether `validate_placeholder` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_placeholder(input_value)
