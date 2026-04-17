import vampytest

from ...core import BUILTIN_EMOJIS
from ...utils import is_url

from ..urls import CDN_ENDPOINT, build_emoji_url_as


def _iter_options():
    emoji_id = 202504170010
    yield (
        emoji_id,
        False,
        None,
        None,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.png',
    )
    
    emoji_id = 202504170011
    yield (
        emoji_id,
        True,
        None,
        None,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.gif',
    )
    
    emoji_id = BUILTIN_EMOJIS['x'].id
    yield (
        emoji_id,
        False,
        None,
        None,
        None,
    )
    
    emoji_id = 202504170012
    yield (
        emoji_id,
        True,
        'png',
        128,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.png?size=128',
    )
    
    emoji_id = 202506200030
    yield (
        emoji_id,
        False,
        'webp',
        None,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.webp',
    )
    
    emoji_id = 202506200031
    yield (
        emoji_id,
        True,
        'webp',
        None,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.webp?animated=true',
    )
    
    emoji_id = 202506200032
    yield (
        emoji_id,
        True,
        'webp',
        128,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.webp?size=128&animated=true',
    )
    
    emoji_id = 202506200033
    yield (
        emoji_id,
        False,
        'avif',
        None,
        f'{CDN_ENDPOINT}/emojis/{emoji_id}.webp',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_emoji_url_as(emoji_id, animated, ext, size):
    """
    Tests whether ``build_emoji_url_as`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Emoji identifier.
    
    animated : `bool`
        Whether the emoji is animated.
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_emoji_url_as(emoji_id, animated, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
