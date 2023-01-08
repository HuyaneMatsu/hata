import warnings

import vampytest

from ....core import BUILTIN_EMOJIS

from ..utils import create_partial_emoji_from_data


def test__create_partial_emoji_from_data__0():
    """
    Tests whether ``create_partial_emoji_from_data`` works as intended.
    """
    emoji_1 = BUILTIN_EMOJIS['x']
    
    emoji = create_partial_emoji_from_data({'name': emoji_1.unicode})
    
    vampytest.assert_is(emoji, emoji_1)


def test__create_partial_emoji_from_data__1():
    """
    Tests whether ``create_partial_emoji_from_data`` handles new unicode emojis correctly.
    
    Issue: `create_partial_emoji_from_data` handled new unicode emoji cases incorrectly.
    """
    unicode_string = 'Aether'
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        
        emoji = create_partial_emoji_from_data({'name': unicode_string})
    
    vampytest.assert_eq(emoji.unicode, unicode_string)
