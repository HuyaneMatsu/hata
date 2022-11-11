import vampytest

from ...core import BUILTIN_EMOJIS
from ...emoji import Emoji

from ..fields import validate_unicode_emoji


def test__validate_unicode_emoji__0():
    """
    Tests whether ``validate_unicode_emoji`` works as intended.
    
    Case: Passing.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    for input_value, expected_output in (
        (None, None),
        (emoji, emoji),
    ):
        output = validate_unicode_emoji(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_unicode_emoji__1():
    """
    Tests whether ``validate_unicode_emoji`` works as intended.
    
    Case: `TypeError`
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_unicode_emoji(input_value)


def test__validate_unicode_emoji__2():
    """
    Tests whether ``validate_unicode_emoji`` works as intended.
    
    Case: `ValueError`
    """
    for input_value in (
        Emoji.precreate(202211020000),
    ):
        with vampytest.assert_raises(ValueError):
            validate_unicode_emoji(input_value)
