import vampytest

from ...sticker import Sticker, StickerFormat
from ...utils import is_url

from ..urls import CDN_ENDPOINT, MEDIA_ENDPOINT, sticker_url


def _iter_options():
    sticker_id = 202406010000
    yield (
        sticker_id,
        StickerFormat.png,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010001
    yield (
        sticker_id,
        StickerFormat.apng,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010002
    yield (
        sticker_id,
        StickerFormat.lottie,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.json',
    )
    
    sticker_id = 202406010003
    yield (
        sticker_id,
        StickerFormat.gif,
        f'{MEDIA_ENDPOINT}/stickers/{sticker_id}.gif',
    )
    
    sticker_id = 202406010011
    yield (
        sticker_id,
        StickerFormat.none,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sticker_url(sticker_id, sticker_format):
    """
    Tests whether ``sticker_url`` works as intended.
    
    Parameters
    ----------
    sticker_id : `int`
        Sticker identifier.
    
    sticker_format : ``StickerFormat``
        Sticker format to create sticker with.
    
    Returns
    -------
    output : `None | str`
    """
    sticker = Sticker.precreate(sticker_id, sticker_format = sticker_format)
    
    output = sticker_url(sticker)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
