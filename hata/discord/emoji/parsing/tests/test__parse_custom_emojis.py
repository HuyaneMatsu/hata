import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..utils import parse_custom_emojis


def test__parse_custom_emojis():
    """
    Tests whether `parse_custom_emojis` works as intended.
    """
    emojis = {
        BUILTIN_EMOJIS['heart'],
        Emoji.precreate(202301010080, name = 'haru', animated = True),
        BUILTIN_EMOJIS['knife'],
        Emoji.precreate(202301010081, name = 'kuroi'),
    }
    text = ' '.join([emoji.as_emoji for emoji in emojis] * 2)
    
    expected_output = {emoji for emoji in emojis if emoji.is_custom_emoji()}
    
    parsed_emojis = parse_custom_emojis(text)
    vampytest.assert_eq(expected_output, parsed_emojis)
