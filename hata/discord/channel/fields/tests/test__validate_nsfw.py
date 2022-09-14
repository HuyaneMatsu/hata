import vampytest

from ..nsfw import validate_nsfw


def test__validate_nsfw__0():
    """
    Tests whether `validate_nsfw` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_nsfw(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_nsfw__1():
    """
    Tests whether `validate_nsfw` works as intended.
    
    Case: type error.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_nsfw(input_value)
