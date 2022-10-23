import vampytest

from ..constants import DESCRIPTION_LENGTH_MAX
from ..fields import validate_description


def test__validate_description__0():
    """
    Tests whether `validate_description` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_description(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_description__1():
    """
    Tests whether `validate_description` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (DESCRIPTION_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_description(input_value)


def test__validate_description__2():
    """
    Tests whether `validate_description` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_description(input_value)
