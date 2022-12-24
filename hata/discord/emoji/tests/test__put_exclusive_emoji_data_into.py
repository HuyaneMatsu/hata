import vampytest

from ...core import BUILTIN_EMOJIS

from ..emoji import Emoji
from ..utils import put_exclusive_emoji_data_into


def test__put_exclusive_emoji_data_into__0():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: builtin emoji.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    data = put_exclusive_emoji_data_into(emoji, {})
    
    vampytest.assert_eq(data, {'emoji_name': emoji.unicode})


def test__put_exclusive_emoji_data_into__1():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: Custom emoji.
    """
    emoji = Emoji.precreate(202209110002)
    
    data = put_exclusive_emoji_data_into(emoji, {})
    
    vampytest.assert_eq(data, {'emoji_id': str(emoji.id)})


def test__put_exclusive_emoji_data_into__2():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: No emoji.
    """
    data = put_exclusive_emoji_data_into(None, {})
    
    vampytest.assert_eq(data, {'emoji_name': None})
