import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..utils import parse_emoji


def test__parse_emoji__coloned_builtin_name():
    """
    Tests whether `parse_emoji` parses builtin emojis with coloned name.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = f':{emoji.name}:'

    parsed_emoji = parse_emoji(text)
    vampytest.assert_is(emoji, parsed_emoji)


def test__parse_emoji__0():
    """
    Tests whether ``parse_emoji`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = Emoji.precreate(202301010089, name = 'replica', animated = True)
        
    for input_value, expected_output in (
        (emoji_0.as_emoji, emoji_0),
        (emoji_1.as_emoji, emoji_1),
    ):
        output = parse_emoji(input_value)
        vampytest.assert_eq(output, expected_output)
