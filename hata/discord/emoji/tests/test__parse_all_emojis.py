import vampytest

from ...core import BUILTIN_EMOJIS, UNICODE_TO_EMOJI

from .. import Emoji, parse_all_emojis, parse_all_emojis_ordered
from ..unicodes import UNICODES


def test__parse_all_emojis__unicode_all__0():
    """
    Tests whether `parse_all_emojis` can parse all the builtin emojis correctly.
    
    Case: unicode
    """
    for unicode in UNICODES:
        emoji = UNICODE_TO_EMOJI[unicode.value]
        
        parsed_emojis = parse_all_emojis(unicode.value)
        
        vampytest.assert_eq({emoji}, parsed_emojis)


def test__parse_all_emojis__custom():
    """
    Tests whether `parse_all_emojis` can parse custom emojis correctly.
    """
    emoji = Emoji.precreate(20220815000000000, name='haru', animated=True)
    parsed_emojis = parse_all_emojis(emoji.as_emoji)
    vampytest.assert_eq({emoji}, parsed_emojis)


def test__parse_all_emojis__unicode_multiple():
    """
    Tests whether `parse_all_emojis` can parse multiple unicode emojis correctly.
    """
    emojis = {BUILTIN_EMOJIS['heart'], BUILTIN_EMOJIS['knife']}
    text = ' '.join(emoji.as_emoji for emoji in emojis)
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq(emojis, parsed_emojis)


def test__parse_all_emojis__mixed():
    """
    Tests whether `parse_all_emojis` parses multiple & multy-kind emojis correctly.
    """
    emojis = {
        BUILTIN_EMOJIS['heart'],
        Emoji.precreate(20220815000000000, name='haru', animated=True),
        BUILTIN_EMOJIS['knife'],
        Emoji.precreate(20220815000000001, name='kuroi'),
    }
    text = ' '.join([emoji.as_emoji for emoji in emojis] * 2)
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq(emojis, parsed_emojis)


def test__parse_all_emojis__coloned_builtin_name__0():
    """
    Tests whether `parse_all_emojis` parses builtin emojis with coloned name.
    
    Case: 1
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    text = f':{emoji_1.name}:'
    
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq({emoji_1}, parsed_emojis)



def test__parse_all_emojis__coloned_builtin_name__1():
    """
    Tests whether `parse_all_emojis` parses builtin emojis with coloned name.
    
    Case: 2
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['leg']
    
    text = f':{emoji_1.name}::{emoji_2.name}:'
    
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq({emoji_1, emoji_2}, parsed_emojis)


def test__parse_all_emojis__coloned_builtin_name__2():
    """
    Tests whether `parse_all_emojis` parses builtin emojis with coloned name.
    
    Case: 2, but first is escaped.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['leg']
    
    text = f'\:{emoji_1.name}::{emoji_2.name}:'
    
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq({emoji_2}, parsed_emojis)


def test__parse_all_emojis__coloned_builtin_name__3():
    """
    Tests whether `parse_all_emojis` parses builtin emojis with coloned name.
    
    Case: 2, but first is escaped at the end.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['leg']
    
    text = f':{emoji_1.name}\::{emoji_2.name}:'
    
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq({emoji_2}, parsed_emojis)


def test__parse_all_emojis__coloned_builtin_name__4():
    """
    Tests whether `parse_all_emojis` parses builtin emojis with coloned name.
    
    Case: 2, but second is escaped.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['leg']
    
    text = f':{emoji_1.name}:\:{emoji_2.name}:'
    
    parsed_emojis = parse_all_emojis(text)
    vampytest.assert_eq({emoji_1}, parsed_emojis)


def test__parse_all_emojis_ordered():
    """
    Tests whether ``parse_all_emojis_ordered`` parses multy-kind emojis correctly.
    """
    emojis = [
        BUILTIN_EMOJIS['heart'],
        Emoji.precreate(20220815000000000, name='haru', animated=True),
        BUILTIN_EMOJIS['knife'],
        Emoji.precreate(20220815000000001, name='kuroi'),
    ]
    text = ' '.join([emoji.as_emoji for emoji in emojis] * 2)
    
    parsed_emojis = parse_all_emojis_ordered(text)
    vampytest.assert_eq(emojis, parsed_emojis)
