import vampytest

from ..moderated import validate_moderated


def test__validate_moderated__0():
    """
    Tests whether `validate_moderated` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_moderated(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_moderated__1():
    """
    Tests whether `validate_moderated` works as intended.
    
    Case: type error.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_moderated(input_value)
