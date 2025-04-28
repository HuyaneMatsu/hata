import vampytest

from ...sticker import StickerPack
from ...utils import is_url

from ..urls import CDN_ENDPOINT, sticker_pack_banner


def _iter_options():
    sticker_pack_id = 2025040140
    banner_id = 2025040141
    yield (
        sticker_pack_id,
        banner_id,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{banner_id}.png',
    )
    
    sticker_pack_id = 2025040142
    banner_id = 2025040143
    yield (
        sticker_pack_id,
        banner_id,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{banner_id}.png',
    )
    
    sticker_pack_id = 2025040144
    banner_id = 0
    yield (
        sticker_pack_id,
        banner_id,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sticker_pack_banner(sticker_pack_id, banner_id):
    """
    Tests whether ``sticker_pack_banner`` works as intended.
    
    Parameters
    ----------
    sticker_pack_id : `int`
        Sticker pack identifier.
    
    banner_id : `int`
        Sticker pack banner identifier.
    
    Returns
    -------
    output : `None | str`
    """
    sticker_pack = StickerPack.precreate(sticker_pack_id, banner_id = banner_id)
    
    output = sticker_pack_banner(sticker_pack)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
