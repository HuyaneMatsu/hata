import vampytest

from ..fields import validate_mentioned_everyone


def test__validate_mentioned_everyone__0():
    """
    Tests whether `validate_mentioned_everyone` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_mentioned_everyone(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_mentioned_everyone__1():
    """
    Tests whether `validate_mentioned_everyone` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_mentioned_everyone(input_value)
