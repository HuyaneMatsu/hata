import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import parse_emoji


def _iter_options():
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202404120000, name = 'love')
    
    yield {}, None
    yield {'poll_media': {'emoji': None}}, None
    yield {'poll_media': {'emoji': {'name': None}}}, None
    yield {'poll_media': {'emoji': {'name': unicode_emoji.unicode}}}, unicode_emoji
    yield {'poll_media': {'emoji': {'name': custom_emoji.name, 'id': str(custom_emoji.id)}}}, custom_emoji


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_emoji(input_data):
    """
    Tests whether ``parse_emoji`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Emoji``
    """
    output = parse_emoji(input_data)
    vampytest.assert_instance(output, Emoji, nullable = True)
    return output
