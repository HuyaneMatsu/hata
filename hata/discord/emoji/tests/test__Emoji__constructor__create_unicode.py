import vampytest

from ...core import BUILTIN_EMOJIS

from .. import Emoji
from ..unicode_type import Unicode


def test__Emoji__create_unicode_0():
    """
    Tests whether ``Emoji._create_unicode`` registers the emoji by name when `register_by_name` parameter is 
    passed as `True`.
    """
    name = '20220811_0000'
    emoticon = '20220811_0001'
    alias = '20220811_0002'
    
    unicode = Unicode(name, b'abs', False, (emoticon, ), (alias, ))
    
    emoji = Emoji._create_unicode(unicode, True)
    
    for alternative_name in (name, emoticon, alias):
        vampytest.assert_in(alternative_name, BUILTIN_EMOJIS)
        vampytest.assert_is(BUILTIN_EMOJIS[alternative_name], emoji)


def test__Emoji__create_unicode_1():
    """
    Tests whether ``Emoji._create_unicode`` will not register the emoji by name when `register_by_name` parameter is
    passed as `False`.
    """
    name = '20220811_0003'
    emoticon = '20220811_0004'
    alias = '20220811_0005'
    
    unicode = Unicode(name, b'abs', False, (emoticon, ), (alias, ))
    
    Emoji._create_unicode(unicode, False)
    
    for alternative_name in (name, emoticon, alias):
        vampytest.assert_not_in(alternative_name, BUILTIN_EMOJIS)
