import vampytest

from ..constants import TITLE_LENGTH_MAX
from ..fields import validate_title


def test__validate_title__0():
    """
    Tests whether `validate_title` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_title(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_title__1():
    """
    Tests whether `validate_title` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (TITLE_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_title(input_value)


def test__validate_title__2():
    """
    Tests whether `validate_title` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_title(input_value)
