import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..fields import parse_emoji


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202301020013, name = 'met')
    
    yield {'emoji': {'name': emoji_0.unicode}}, emoji_0
    yield {'emoji': {'name': emoji_1.name, 'id': str(emoji_1.id)}}, emoji_1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_emoji(input_data):
    """
    Tests whether ``parse_emoji`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse emoji form.
    """
    return parse_emoji(input_data)
