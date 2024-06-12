import vampytest

from ...sticker import Sticker, StickerFormat

from ..urls import CDN_ENDPOINT, MEDIA_ENDPOINT, sticker_url


def _iter_options():
    sticker_id = 202406010000
    yield (
        Sticker.precreate(sticker_id, sticker_format = StickerFormat.png),
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010001
    yield (
        Sticker.precreate(sticker_id, sticker_format = StickerFormat.apng),
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010002
    yield (
        Sticker.precreate(sticker_id, sticker_format = StickerFormat.lottie),
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.json',
    )
    
    sticker_id = 202406010003
    yield (
        Sticker.precreate(sticker_id, sticker_format = StickerFormat.gif),
        f'{MEDIA_ENDPOINT}/stickers/{sticker_id}.gif',
    )
    
    sticker_id = 202406010011
    yield (
        Sticker.precreate(sticker_id, sticker_format = StickerFormat.none),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sticker_url(sticker):
    """
    Tests whether ``sticker_url`` works as intended.
    
    Parameters
    ----------
    sticker : ``Sticker``
        Sticker to get its url of.
    
    Returns
    -------
    output : `None | str`
    """
    output = sticker_url(sticker)
    vampytest.assert_instance(output, str, nullable = True)
    return output
