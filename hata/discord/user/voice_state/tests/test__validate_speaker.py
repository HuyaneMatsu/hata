import vampytest

from ..fields import validate_speaker


def test__validate_speaker__0():
    """
    Tests whether `validate_speaker` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False),
    ):
        output = validate_speaker(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_speaker__1():
    """
    Tests whether `validate_speaker` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_speaker(input_value)
