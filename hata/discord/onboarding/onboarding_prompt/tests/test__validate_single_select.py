import vampytest

from ..fields import validate_single_select


def test__validate_single_select__0():
    """
    Tests whether `validate_single_select` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_single_select(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_single_select__1():
    """
    Tests whether `validate_single_select` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_single_select(input_value)
