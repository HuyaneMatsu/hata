import vampytest

from ...core import BUILTIN_EMOJIS

from .. import create_partial_emoji_from_data


def test__create_partial_emoji_from_data():
    """
    Tests whether ``create_partial_emoji_from_data`` prefers the `emoji_` prefix format over the one with prefix one.
    """
    emoji_1 = BUILTIN_EMOJIS['x']
    emoji_2 = BUILTIN_EMOJIS['heart']
    
    emoji = create_partial_emoji_from_data({'name': emoji_1.unicode, 'emoji_name': emoji_2.unicode})
    
    vampytest.assert_is(emoji, emoji_2)
