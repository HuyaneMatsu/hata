import vampytest

from ..constants import EMBED_AUTHOR_NAME_LENGTH_MAX
from ..fields import validate_name


def test__validate_name__0():
    """
    Tests whether `validate_name` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
        (1, '1'),
    ):
        output = validate_name(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_name__1():
    """
    Tests whether `validate_name` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (EMBED_AUTHOR_NAME_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_name(input_value)
