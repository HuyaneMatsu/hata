import vampytest

from ...sticker import Sticker, StickerFormat
from ...utils import is_url

from ..urls import CDN_ENDPOINT, MEDIA_ENDPOINT, sticker_url_as


def _iter_options():
    sticker_id = 202406010004
    yield (
        sticker_id,
        StickerFormat.png,
        {},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010005
    yield (
        sticker_id,
        StickerFormat.png,
        {'size': 1024},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?size=1024',
    )
    
    sticker_id = 202406010012
    yield (
        sticker_id,
        StickerFormat.lottie,
        {'size': 1024},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.json',
    )
    
    sticker_id = 202406010006
    yield (
        sticker_id,
        StickerFormat.gif,
        {},
        f'{MEDIA_ENDPOINT}/stickers/{sticker_id}.gif',
    )
    
    sticker_id = 202406010007
    yield (
        sticker_id,
        StickerFormat.png,
        {'preview': True},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png',
    )
    
    sticker_id = 202406010008
    yield (
        sticker_id,
        StickerFormat.apng,
        {'preview': True},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?passthrough=false',
    )
    
    sticker_id = 202406010009
    yield (
        sticker_id,
        StickerFormat.apng,
        {'size': 1024, 'preview': True},
        f'{CDN_ENDPOINT}/stickers/{sticker_id}.png?size=1024&passthrough=false',
    )
    
    sticker_id = 202406010010
    yield (
        sticker_id,
        StickerFormat.none,
        {},
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sticker_url_as(sticker_id, sticker_format, keyword_parameters):
    """
    Tests whether ``sticker_url_as`` works as intended.
    
    Parameters
    ----------
    sticker_id : `int`
        Sticker identifier.
    
    sticker_format : ``StickerFormat``
        Sticker format to create sticker with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    sticker = Sticker.precreate(sticker_id, sticker_format = sticker_format)
    
    output = sticker_url_as(sticker, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
