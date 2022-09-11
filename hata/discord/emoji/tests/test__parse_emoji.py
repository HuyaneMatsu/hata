import vampytest

from ...core import BUILTIN_EMOJIS

from .. import parse_emoji


def test__parse_emoji__coloned_builtin_name():
    """
    Tests whether `parse_emoji` parses builtin emojis with coloned name.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = f':{emoji.name}:'

    parsed_emoji = parse_emoji(text)
    vampytest.assert_is(emoji, parsed_emoji)
