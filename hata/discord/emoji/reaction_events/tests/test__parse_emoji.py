import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import parse_emoji


def test__parse_emoji():
    """
    Tests whether ``parse_emoji`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202301020013, name = 'met')
    
    for input_value, expected_output in (
        ({'emoji': {'name': emoji_0.unicode}}, emoji_0),
        ({'emoji': {'name': emoji_1.name, 'id': str(emoji_1.id)}}, emoji_1),
    ):
        output = parse_emoji(input_value)
        vampytest.assert_is(output, expected_output)
