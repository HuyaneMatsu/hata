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
