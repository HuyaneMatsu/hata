import vampytest

from ...core import BUILTIN_EMOJIS

from .. import Emoji, put_partial_emoji_data_into


def test__put_partial_emoji_data_into__0():
    """
    Tests whether ``put_partial_emoji_data_into`` allows `None`.
    """
    data = {}
    
    put_partial_emoji_data_into(None, data)
    
    vampytest.assert_eq(data, {'emoji_name': None})


def test__put_partial_emoji_data_into__1():
    """
    Tests whether ``put_partial_emoji_data_into`` works as intended for a unicode emoji.
    """
    data = {}
    emoji = BUILTIN_EMOJIS['heart']
    
    put_partial_emoji_data_into(emoji, data)
    
    vampytest.assert_in('emoji_name', data)


def test__put_partial_emoji_data_into__2():
    """
    Tests whether ``put_partial_emoji_data_into`` works as intended for a unicode emoji.
    """
    data = {}
    emoji = Emoji.precreate(202209090000, name = 'Eliminator')
    
    put_partial_emoji_data_into(emoji, data)
    
    vampytest.assert_in('emoji_name', data)
    vampytest.assert_in('emoji_id', data)
