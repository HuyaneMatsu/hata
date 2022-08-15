import vampytest

from ...core import BUILTIN_EMOJIS, UNICODE_TO_EMOJI

from .. import Emoji, parse_all_emojis, parse_all_emojis_ordered


def test__parse_all_emojis__unicode_all():
    """
    Tests whether `parse_all_emojis` can parse all the unicode emojis correctly.
    """
    for emoji in UNICODE_TO_EMOJI.values():
        parsed_emojis = parse_all_emojis(emoji.as_emoji)
        
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
    Tests whether `parse_all_emojis` parsers multiple & multy-kind emojis correctly.
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
