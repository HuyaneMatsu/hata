import vampytest

from ..constants import APPLICATION_COMMAND_NAME_LENGTH_MAX

from ..fields import validate_name


def test__validate_name__0():
    """
    Tests whether `validate_name` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('aa', 'aa'),
    ):
        output = validate_name(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_name__1():
    """
    Tests whether `validate_name` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (APPLICATION_COMMAND_NAME_LENGTH_MAX + 1),
        'ááá',
    ):
        with vampytest.assert_raises(ValueError):
            validate_name(input_value)


def test__validate_name__2():
    """
    Tests whether `validate_name` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_name(input_value)
