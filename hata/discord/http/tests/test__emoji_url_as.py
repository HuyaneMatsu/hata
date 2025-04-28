import vampytest

from ...core import BUILTIN_EMOJIS
from ...emoji import Emoji
from ...utils import is_url

from ..urls import CDN_ENDPOINT, emoji_url_as


def _iter_options():
    emoji_id = 202504170010
    yield (
        emoji_id,
        False,
        {},
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.png',
    )
    
    emoji_id = 202504170011
    yield (
        emoji_id,
        True,
        {},
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.gif',
    )
    
    emoji_id = BUILTIN_EMOJIS['x'].id
    yield (
        emoji_id,
        False,
        {},
        None,
    )
    
    emoji_id = 202504170012
    yield (
        emoji_id,
        True,
        {'ext': 'png', 'size': 128},
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.png?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__emoji_url_as(emoji_id, animated, keyword_parameters):
    """
    Tests whether ``emoji_url_as`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Emoji identifier.
    
    animated : `bool`
        Whether the emoji is animated.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    emoji = Emoji.precreate(emoji_id, animated = animated)
    
    output = emoji_url_as(emoji, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
