import vampytest

from ..fields import validate_discoverable


def test__validate_discoverable__0():
    """
    Tests whether `validate_discoverable` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, True),
        (True, True),
        (False, False)
    ):
        output = validate_discoverable(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_discoverable__1():
    """
    Tests whether `validate_discoverable` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_discoverable(input_value)
