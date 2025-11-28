import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_invite_cover_url_as


def _iter_options():
    application_id = 202511110003
    image_invite_cover = '566666'
    yield (
        application_id,
        image_invite_cover,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_invite_cover}.png',
    )
    
    application_id = 0
    image_invite_cover = '566666'
    yield (
        application_id,
        image_invite_cover,
        None,
        None,
        None,
    )
    
    application_id = 202511110004
    image_invite_cover = 'reisen'
    yield (
        application_id,
        image_invite_cover,
        None,
        None,
        None,
    )
    
    application_id = 202511110005
    image_invite_cover = None
    yield (
        application_id,
        image_invite_cover,
        None,
        None,
        None,
    )
    
    application_id = 202511110006
    image_invite_cover = '566666'
    yield (
        application_id,
        image_invite_cover,
        'jpg',
        128,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_invite_cover}.jpg?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_invite_cover_url_as(application_id, image_invite_cover, ext, size):
    """
    Tests whether ``build_activity_asset_image_invite_cover_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_invite_cover : `None | str`
        The activity's asset's invite_cover image's value.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_invite_cover_url_as(application_id, image_invite_cover, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
