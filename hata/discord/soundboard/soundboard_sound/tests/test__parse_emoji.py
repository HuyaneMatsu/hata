import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import parse_emoji


def test__parse_emoji():
    """
    Tests whether ``parse_emoji`` works as intended.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202305240006, name = 'Yukari')
    
    for input_data, expected_output in (
        ({}, None),
        ({'emoji_name': None}, None),
        ({'emoji_name': unicode_emoji.unicode}, unicode_emoji),
        ({'emoji_name': custom_emoji.name, 'emoji_id': str(custom_emoji.id)}, custom_emoji),
    ):
        output = parse_emoji(input_data)
        vampytest.assert_is(output, expected_output)
