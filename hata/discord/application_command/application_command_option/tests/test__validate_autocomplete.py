import vampytest

from ..fields import validate_autocomplete

from ..preinstanced import ApplicationCommandOptionType

def test__validate_autocomplete__0():
    """
    Tests whether `validate_autocomplete` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_autocomplete(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_autocomplete__1():
    """
    Tests whether `validate_autocomplete` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_autocomplete(input_value)


def test__validate_autocomplete__2():
    """
    Tests whether `validate_autocomplete` works as intended.
    
    Case: `ValueError`.
    """
    with vampytest.assert_raises(ValueError):
        validate_autocomplete(True, ApplicationCommandOptionType.sub_command)
