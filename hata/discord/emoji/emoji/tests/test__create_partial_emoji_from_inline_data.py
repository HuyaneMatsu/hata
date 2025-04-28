from warnings import catch_warnings, simplefilter as apply_simple_filter

import vampytest

from ....core import BUILTIN_EMOJIS

from ..utils import create_partial_emoji_from_inline_data


def test__create_partial_emoji_from_inline_data__0():
    """
    Tests whether ``create_partial_emoji_from_inline_data`` works as intended.
    """
    emoji_2 = BUILTIN_EMOJIS['heart']
    
    emoji = create_partial_emoji_from_inline_data({'emoji_name': emoji_2.unicode})
    
    vampytest.assert_is(emoji, emoji_2)


def test__create_partial_emoji_from_inline_data__1():
    """
    Tests whether ``create_partial_emoji_from_inline_data`` handles new unicode emojis correctly.
    
    Issue: `create_partial_emoji_from_inline_data` handled new unicode emoji cases incorrectly.
    """
    unicode_string = 'Aether'
    
    with catch_warnings():
        apply_simple_filter('ignore')
        
        emoji = create_partial_emoji_from_inline_data({'emoji_name': unicode_string})
    
    vampytest.assert_eq(emoji.unicode, unicode_string)
