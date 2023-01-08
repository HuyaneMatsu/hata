import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_emoji_into


def test__put_emoji_into():
    """
    Tests whether ``put_emoji_into`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202301020014, name = 'met')
    
    for input_value, expected_output in (
        (emoji_0, {'emoji': {'name': emoji_0.unicode}},),
        (emoji_1, {'emoji': {'name': emoji_1.name, 'id': str(emoji_1.id)}}),
    ):
        output = put_emoji_into(input_value, {}, False)
        vampytest.assert_eq(output, expected_output)
