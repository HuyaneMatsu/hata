import vampytest

from ....core import BUILTIN_EMOJIS

from ..emoji import Emoji
from ..utils import put_exclusive_emoji_data_into


def test__put_exclusive_emoji_data_into__unicode_emoji():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: unicode emoji.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    data = put_exclusive_emoji_data_into(emoji, {})
    
    vampytest.assert_eq(data, {'name': emoji.unicode})


def test__put_exclusive_emoji_data_into__custom_emoji():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: Custom emoji.
    """
    emoji = Emoji.precreate(202404130003)
    
    data = put_exclusive_emoji_data_into(emoji, {})
    
    vampytest.assert_eq(data, {'id': str(emoji.id)})


def test__put_exclusive_emoji_data_into__no_emoji():
    """
    Tests whether ``put_exclusive_emoji_data_into`` works as intended.
    
    Case: No emoji.
    """
    data = put_exclusive_emoji_data_into(None, {})
    
    vampytest.assert_eq(data, {'name': None})
