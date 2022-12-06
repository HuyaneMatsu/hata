import vampytest

from ..constants import KEY_LENGTH_MAX

from ..fields import validate_key


def test__validate_key__0():
    """
    Tests whether `validate_key` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('a', 'a'),
    ):
        output = validate_key(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_key__1():
    """
    Tests whether `validate_key` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (KEY_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_key(input_value)


def test__validate_key__2():
    """
    Tests whether `validate_key` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_key(input_value)
