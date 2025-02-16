import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_default_thread_reaction_emoji


def _iter_options():
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202209110004)
    
    yield None, False, {}
    yield None, True, {'default_reaction_emoji': None}
    yield unicode_emoji, False, {'default_reaction_emoji': {'emoji_name': unicode_emoji.unicode}}
    yield unicode_emoji, True, {'default_reaction_emoji': {'emoji_name': unicode_emoji.unicode}}
    yield custom_emoji, False, {'default_reaction_emoji': {'emoji_id': str(custom_emoji.id)}}
    yield custom_emoji, True, {'default_reaction_emoji': {'emoji_id': str(custom_emoji.id)}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_thread_reaction_emoji(input_value, defaults):
    """
    Tests whether ``put_default_thread_reaction_emoji`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | Emoji`
        Value to serialize.
    defaults : `bool`
        Whether values with their value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """    
    return put_default_thread_reaction_emoji(input_value, {}, defaults)
