import vampytest

from ..urls import CDN_ENDPOINT, build_sticker_pack_banner_url_as


def _iter_options():
    sticker_pack_banner_id = 2025040151
    
    yield (
        sticker_pack_banner_id,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.png',
    )
    
    sticker_pack_banner_id = 2025040153
    
    yield (
        sticker_pack_banner_id,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.png',
    )
    
    sticker_pack_banner_id = 0
    
    yield (
        sticker_pack_banner_id,
        None,
        None,
        None,
    )
    
    sticker_pack_banner_id = 2025040157
    
    yield (
        sticker_pack_banner_id,
        'jpg',
        128,
        f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.jpg?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_sticker_pack_banner_url_as(sticker_pack_banner_id, ext, size):
    """
    Tests whether ``build_sticker_pack_banner_url_as`` works as intended.
    
    Parameters
    ----------
    sticker_pack_banner_id : `int`
        Sticker pack banner identifier.
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_sticker_pack_banner_url_as(sticker_pack_banner_id, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
