import warnings as module_warnings

import vampytest

from ....core import BUILTIN_EMOJIS

from ..emoji import Emoji
from ..utils import create_unicode_emoji


def test__create_unicode_emoji__0():
    """
    Tests whether ``create_unicode_emoji`` works as intended.
    
    Case: found.
    """
    emoji = BUILTIN_EMOJIS['x']
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        output = create_unicode_emoji(emoji.unicode)
        
        vampytest.assert_eq(len(warnings), 0)
    
    vampytest.assert_is(output, emoji)



def test__create_unicode_emoji__1():
    """
    Tests whether ``create_unicode_emoji`` works as intended.
    
    Case: not found.
    """
    unicode = '20230101_0003'
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        output = create_unicode_emoji(unicode)
        
        vampytest.assert_eq(len(warnings), 1)
    
    vampytest.assert_instance(output, Emoji)
    vampytest.assert_eq(output.unicode, unicode)
