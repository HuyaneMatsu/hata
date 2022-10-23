import vampytest

from ..constants import VALUE_LENGTH_MAX
from ..fields import validate_label


def test__validate_label__0():
    """
    Tests whether `validate_label` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('orindance.party', 'orindance.party'),
    ):
        output = validate_label(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_label__1():
    """
    Tests whether `validate_label` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (VALUE_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_label(input_value)


def test__validate_label__2():
    """
    Tests whether `validate_label` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_label(input_value)
