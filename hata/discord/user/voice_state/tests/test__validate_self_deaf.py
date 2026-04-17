import vampytest

from ..fields import validate_self_deaf


def test__validate_self_deaf__0():
    """
    Tests whether `validate_self_deaf` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False),
    ):
        output = validate_self_deaf(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_self_deaf__1():
    """
    Tests whether `validate_self_deaf` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_self_deaf(input_value)
