import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import parse_default_thread_reaction_emoji


def _iter_options():
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202209110005)
    
    yield {}, None
    yield {'default_reaction_emoji': None}, None
    yield {'default_reaction_emoji': {'emoji_name': None}}, None
    yield {'default_reaction_emoji': {'emoji_name': unicode_emoji.unicode}}, unicode_emoji
    yield {'default_reaction_emoji': {'emoji_id': str(custom_emoji.id)}}, custom_emoji


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_thread_reaction_emoji(input_data):
    """
    Tests whether ``parse_default_thread_reaction_emoji`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Emoji``
    """
    output = parse_default_thread_reaction_emoji(input_data)
    vampytest.assert_instance(output, Emoji, nullable = True)
    return output
