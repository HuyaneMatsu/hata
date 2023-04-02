import vampytest

from ..constants import EMBED_FIELD_VALUE_LENGTH_MAX
from ..fields import validate_value


def test__validate_value__0():
    """
    Tests whether `validate_value` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
        (1, '1'),
    ):
        output = validate_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_value__1():
    """
    Tests whether `validate_value` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (EMBED_FIELD_VALUE_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_value(input_value)
