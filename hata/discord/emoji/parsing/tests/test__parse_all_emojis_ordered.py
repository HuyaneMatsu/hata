import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..utils import parse_all_emojis_ordered


def test__parse_all_emojis__ordered():
    """
    Tests whether ``parse_all_emojis_ordered`` works as intended.
    """
    emojis = [
        BUILTIN_EMOJIS['heart'],
        Emoji.precreate(202301010082, name = 'haru', animated = True),
        BUILTIN_EMOJIS['knife'],
        Emoji.precreate(202301010083, name = 'kuroi'),
    ]
    text = ' '.join([emoji.as_emoji for emoji in emojis] * 2)
    
    parsed_emojis = parse_all_emojis_ordered(text)
    vampytest.assert_eq(emojis, parsed_emojis)
