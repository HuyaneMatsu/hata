import vampytest

from ....core import BUILTIN_EMOJIS

from ..emoji import Emoji
from ..utils import create_emoji_from_exclusive_data


def test__create_emoji_from_exclusive_data__unicode_emoji():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: unicode emoji.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    data = {'name': emoji.unicode}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(emoji, output_emoji)


def test__create_emoji_from_exclusive_data__custom_emoji():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: Custom emoji.
    """
    emoji = Emoji.precreate(202404130000)
    
    data = {'id': str(emoji.id)}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(emoji, output_emoji)


def test__create_emoji_from_exclusive_data__no_emoji():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: No emoji.
    """
    data = {}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(None, output_emoji)


def test__create_emoji_from_exclusive_data__no_overwrite():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: Do not overwrite name & animated when created from id.
    """
    emoji_id = 202404130001
    emoji_name = 'warning'
    emoji_animated = True
    guild_id = 202404130002
    
    # Keep it for the cache, dont be dumb!
    original_emoji = Emoji.from_data(
        {
            'id': str(emoji_id),
            'name': emoji_name,
            'animated': emoji_animated,
        },
        guild_id,
    )
    
    data = {'id': str(emoji_id)}
    
    emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_eq(emoji.name, emoji_name)
    vampytest.assert_eq(emoji.animated, emoji_animated)
