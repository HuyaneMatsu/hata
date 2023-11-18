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
    
    debug_logger_called = False
    def call_debug_logger(message, unique):
        nonlocal debug_logger_called
        debug_logger_called = True
    
    mocked = vampytest.mock_globals(
        create_unicode_emoji,
        ALLOW_DEBUG_MESSAGES = True,
        call_debug_logger = call_debug_logger
    )
    
    output = mocked(emoji.unicode)
    
    vampytest.assert_is(output, emoji)
    vampytest.assert_false(debug_logger_called)



def test__create_unicode_emoji__1():
    """
    Tests whether ``create_unicode_emoji`` works as intended.
    
    Case: not found.
    """
    unicode = '20230101_0003'
    
    debug_logger_called = False
    def call_debug_logger(message, unique):
        nonlocal debug_logger_called
        debug_logger_called = True
    
    mocked = vampytest.mock_globals(
        create_unicode_emoji,
        ALLOW_DEBUG_MESSAGES = True,
        call_debug_logger = call_debug_logger
    )
    
    output = mocked(unicode)
        
    vampytest.assert_instance(output, Emoji)
    vampytest.assert_eq(output.unicode, unicode)
    vampytest.assert_true(debug_logger_called)
