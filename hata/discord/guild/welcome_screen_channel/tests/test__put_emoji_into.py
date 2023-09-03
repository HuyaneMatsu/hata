import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_emoji_into


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202212230006, name = 'met')
    
    yield None, False, {}
    yield None, True, {'emoji_name': None}
    yield emoji_0, False, {'emoji_name': emoji_0.unicode}
    yield emoji_1, False, {'emoji_name': emoji_1.name, 'emoji_id': str(emoji_1.id)}
    yield emoji_0, True, {'emoji_name': emoji_0.unicode}
    yield emoji_1, True, {'emoji_name': emoji_1.name, 'emoji_id': str(emoji_1.id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_emoji_into(input_value, defaults):
    """
    Tests whether ``put_emoji_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``Emoji``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_emoji_into(input_value, {}, defaults)
