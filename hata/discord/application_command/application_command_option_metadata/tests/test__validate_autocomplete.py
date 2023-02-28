import vampytest

from ..fields import validate_autocomplete

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
