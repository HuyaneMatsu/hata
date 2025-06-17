import vampytest

from ...core import BUILTIN_EMOJIS
from ...utils import is_url

from ..urls import CDN_ENDPOINT, build_emoji_url


def _iter_options():
    emoji_id = 202504170000
    yield (
        emoji_id,
        False,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.png',
    )
    
    emoji_id = 202504170001
    yield (
        emoji_id,
        True,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.gif',
    )
    
    emoji_id = BUILTIN_EMOJIS['x'].id
    yield (
        emoji_id,
        False,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_emoji_url(emoji_id, animated):
    """
    Tests whether ``build_emoji_url`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Emoji identifier.
    
    animated : `bool`
        Whether the emoji is animated.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_emoji_url(emoji_id, animated)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
