import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_emoji


def _iter_options():
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202404120001, name = 'love')
    
    yield None, False, {}
    yield None, True, {'poll_media': {'emoji': None}}
    yield unicode_emoji, False, {'poll_media': {'emoji': {'name': unicode_emoji.unicode}}}
    yield unicode_emoji, True, {'poll_media': {'emoji': {'name': unicode_emoji.unicode}}}
    yield custom_emoji, False, {'poll_media': {'emoji': {'name': custom_emoji.name, 'id': str(custom_emoji.id)}}}
    yield custom_emoji, True, {'poll_media': {'emoji': {'name': custom_emoji.name, 'id': str(custom_emoji.id)}}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_emoji(input_value, defaults):
    """
    Tests whether ``put_emoji`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | Emoji``
        Value to serialize.
    defaults : `bool`
        Whether values with their value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """    
    return put_emoji(input_value, {}, defaults)
