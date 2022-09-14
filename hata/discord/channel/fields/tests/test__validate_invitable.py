import vampytest

from ..invitable import validate_invitable


def test__validate_invitable__0():
    """
    Tests whether `validate_invitable` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_invitable(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_invitable__1():
    """
    Tests whether `validate_invitable` works as intended.
    
    Case: type error.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_invitable(input_value)
