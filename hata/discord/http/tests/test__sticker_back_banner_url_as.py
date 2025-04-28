import vampytest

from ...sticker import StickerPack
from ...utils import is_url

from ..urls import CDN_ENDPOINT, sticker_pack_banner_as


def _iter_options():
    sticker_pack_id = 2025040150
    banner_id = 2025040151
    yield (
        sticker_pack_id,
        banner_id,
        {},
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{banner_id}.png',
    )
    
    sticker_pack_id = 2025040152
    banner_id = 2025040153
    yield (
        sticker_pack_id,
        banner_id,
        {},
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{banner_id}.png',
    )
    
    sticker_pack_id = 2025040154
    banner_id = 0
    yield (
        sticker_pack_id,
        banner_id,
        {},
        None,
    )
    
    sticker_pack_id = 2025040156
    banner_id = 2025040157
    yield (
        sticker_pack_id,
        banner_id,
        {'ext': 'jpg', 'size': 128},
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{banner_id}.jpg?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sticker_pack_banner_as(sticker_pack_id, banner_id, keyword_parameters):
    """
    Tests whether ``sticker_pack_banner_as`` works as intended.
    
    Parameters
    ----------
    sticker_pack_id : `int`
        Sticker pack identifier.
    
    banner_id : `int`
        Sticker pack banner identifier.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    sticker_pack = StickerPack.precreate(sticker_pack_id, banner_id = banner_id)
    
    output = sticker_pack_banner_as(sticker_pack, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
