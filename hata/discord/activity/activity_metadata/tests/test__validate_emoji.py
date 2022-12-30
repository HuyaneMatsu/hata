import vampytest

from ....core import BUILTIN_EMOJIS

from ..fields import validate_emoji


def test__validate_emoji__0():
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: Passing.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    for input_value, expected_output in (
        (None, None),
        (emoji, emoji),
    ):
        output = validate_emoji(input_value)
        vampytest.assert_is(output, expected_output)



def test__validate_emoji__1():
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_emoji(input_value)
