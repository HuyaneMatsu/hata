import vampytest

from ....emoji import Emoji

from ..fields import validate_emoji


def test__validate_emoji__0():
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: passing.
    """
    emoji = Emoji.precreate(202210040002)
    
    for input_parameter, expected_output in (
        (None, None),
        (emoji, emoji),
    ):
        output = validate_emoji(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_emoji__1():
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_emoji(input_parameter)
