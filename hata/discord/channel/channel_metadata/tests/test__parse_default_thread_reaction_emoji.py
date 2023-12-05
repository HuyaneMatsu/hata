import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import parse_default_thread_reaction_emoji


def test__parse_default_thread_reaction_emoji():
    """
    Tests whether ``parse_default_thread_reaction_emoji`` works as intended.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202209110004)
    
    for input_data, expected_output in (
        ({}, None),
        ({'default_reaction_emoji': None}, None),
        ({'default_reaction_emoji': {'emoji_name': None}}, None),
        ({'default_reaction_emoji': {'emoji_name': unicode_emoji.unicode}}, unicode_emoji),
        ({'default_reaction_emoji': {'emoji_id': str(custom_emoji.id)}}, custom_emoji),
    ):
        output = parse_default_thread_reaction_emoji(input_data)
        vampytest.assert_is(output, expected_output)
