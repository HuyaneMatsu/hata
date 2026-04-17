import vampytest

from ..urls import CDN_ENDPOINT, build_sticker_pack_banner_url


def _iter_options():
    sticker_pack_banner_id = 2025040141
    
    yield (
        sticker_pack_banner_id,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.png',
    )
    
    sticker_pack_banner_id = 2025040143
    
    yield (
        sticker_pack_banner_id,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.png',
    )
    
    sticker_pack_banner_id = 0
    
    yield (
        sticker_pack_banner_id,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_sticker_pack_banner_url(sticker_pack_banner_id):
    """
    Tests whether ``build_sticker_pack_banner_url`` works as intended.
    
    Parameters
    ----------
    sticker_pack_banner_id : `int`
        Sticker pack banner identifier.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_sticker_pack_banner_url(sticker_pack_banner_id)
    vampytest.assert_instance(output, str, nullable = True)
    return output
