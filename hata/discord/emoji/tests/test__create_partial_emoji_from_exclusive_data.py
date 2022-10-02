import vampytest

from ...core import BUILTIN_EMOJIS

from .. import Emoji, create_emoji_from_exclusive_data


def test__create_emoji_from_exclusive_data__0():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: builtin emoji.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    data = {'emoji_name': emoji.unicode}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(emoji, output_emoji)


def test__create_emoji_from_exclusive_data__1():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: Custom emoji.
    """
    emoji = Emoji.precreate(202209110001)
    
    data = {'emoji_id': str(emoji.id)}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(emoji, output_emoji)


def test__create_emoji_from_exclusive_data__2():
    """
    Tests whether ``create_emoji_from_exclusive_data`` works as intended.
    
    Case: No emoji.
    """
    data = {}
    
    output_emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_is(None, output_emoji)


def test__create_emoji_from_exclusive_data__3():
    """
    Issue: `create_emoji_from_exclusive_data` overwrote emoji name & animated.
    """
    emoji_id = 202209250000
    emoji_name = 'warning'
    emoji_animated = True
    guild_id = 202209250001
    
    # Keep it for the cache, dont be dumb!
    original_emoji = Emoji(
        {
            'id': str(emoji_id),
            'name': emoji_name,
            'animated': emoji_animated,
        },
        guild_id,
    )
    
    data = {'emoji_id': str(emoji_id)}
    
    emoji = create_emoji_from_exclusive_data(data)
    
    vampytest.assert_eq(emoji.name, emoji_name)
    vampytest.assert_eq(emoji.animated, emoji_animated)
