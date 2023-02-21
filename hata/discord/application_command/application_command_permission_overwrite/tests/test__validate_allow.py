import vampytest

from ..fields import validate_allow


def test__validate_allow__0():
    """
    Tests whether `validate_allow` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_allow(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_allow__1():
    """
    Tests whether `validate_allow` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_allow(input_value)
