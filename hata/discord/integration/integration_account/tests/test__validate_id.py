import vampytest

from ..constants import ID_LENGTH_MAX
from ..fields import validate_id


def test__validate_id__0():
    """
    Tests whether `validate_id` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('', ''),
        ('a', 'a'),
    ):
        output = validate_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_id__1():
    """
    Tests whether `validate_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (ID_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_id(input_value)


def test__validate_id__2():
    """
    Tests whether `validate_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_id(input_value)
