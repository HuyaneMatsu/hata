import vampytest

from ..emoji import Emoji
from ..utils import create_partial_emoji_from_id


def test__create_partial_emoji_from_id__0():
    """
    Tests whether ``create_partial_emoji_from_id`` works as intended.
    
    Case: output.
    """
    emoji_id = 202301010077
    emoji = create_partial_emoji_from_id(emoji_id)
    
    vampytest.assert_instance(emoji, Emoji)
    vampytest.assert_eq(emoji.id, emoji_id)


def test__create_partial_emoji_from_id__1():
    """
    Tests whether ``create_partial_emoji_from_id`` works as intended.
    
    Case: caching.
    """
    emoji_id = 202301010079
    emoji = create_partial_emoji_from_id(emoji_id)
    test_emoji = create_partial_emoji_from_id(emoji_id)
    vampytest.assert_is(emoji, test_emoji)
