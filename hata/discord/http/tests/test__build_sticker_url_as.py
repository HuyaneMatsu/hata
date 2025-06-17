import vampytest

from ...sticker import StickerFormat

from ..urls import CDN_ENDPOINT, MEDIA_ENDPOINT, build_sticker_url_as


def _iter_options():
    sticker_id = 202406010004
    yield (
        sticker_id,
        StickerFormat.png,
        None,
        False,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010005
    yield (
        sticker_id,
        StickerFormat.png,
        1024,
        False,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?size=1024',
    )
    
    sticker_id = 202406010012
    yield (
        sticker_id,
        StickerFormat.lottie,
        1024,
        False,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.json',
    )
    
    sticker_id = 202406010006
    yield (
        sticker_id,
        StickerFormat.gif,
        None,
        None,
        f'{MEDIA_ENDPOINT}/stickers/{sticker_id}.gif',
    )
    
    sticker_id = 202406010007
    yield (
        sticker_id,
        StickerFormat.png,
        None,
        True,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010008
    yield (
        sticker_id,
        StickerFormat.apng,
        None,
        True,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?passthrough=false',
    )
    
    sticker_id = 202406010009
    yield (
        sticker_id,
        StickerFormat.apng,
        1024,
        True,
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?size=1024&passthrough=false',
    )
    
    sticker_id = 202406010010
    yield (
        sticker_id,
        StickerFormat.none,
        None,
        None,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_sticker_url_as(sticker_id, sticker_format, size, preview):
    """
    Tests whether ``build_sticker_url_as`` works as intended.
    
    Parameters
    ----------
    sticker_id : `int`
        The sticker's identifier.
    
    sticker_format : ``StickerFormat``
        The sticker's format.
    
    size : `None | int`
        The preferred minimal size of the icon's url.
    
    preview : `bool`
        Whether preview url should be generated.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_sticker_url_as(sticker_id, sticker_format, size, preview)
    vampytest.assert_instance(output, str, nullable = True)
    return output
