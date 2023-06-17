import vampytest

from ..fields import validate_large


def test__validate_large__0():
    """
    Tests whether `validate_large` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_large(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_large__1():
    """
    Tests whether `validate_large` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_large(input_value)
