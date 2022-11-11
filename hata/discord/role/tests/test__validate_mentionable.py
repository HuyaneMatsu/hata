import vampytest

from ..fields import validate_mentionable


def test__validate_mentionable__0():
    """
    Tests whether `validate_mentionable` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_mentionable(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_mentionable__1():
    """
    Tests whether `validate_mentionable` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_mentionable(input_value)
