import vampytest

from ..fields import validate_default


def test__validate_default__0():
    """
    Tests whether `validate_default` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_default(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_default__1():
    """
    Tests whether `validate_default` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_default(input_value)
