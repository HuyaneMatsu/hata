import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_large_url_as


def _iter_options():
    application_id = 202504170050
    image_large = '566666'
    yield (
        application_id,
        image_large,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.png',
    )
    
    application_id = 0
    image_large = '566666'
    yield (
        application_id,
        image_large,
        None,
        None,
        None,
    )
    
    application_id = 202504170051
    image_large = 'reisen'
    yield (
        application_id,
        image_large,
        None,
        None,
        None,
    )
    
    application_id = 202504170052
    image_large = None
    yield (
        application_id,
        image_large,
        None,
        None,
        None,
    )
    
    application_id = 202504170053
    image_large = '566666'
    yield (
        application_id,
        image_large,
        'jpg',
        128,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.jpg?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_large_url_as(application_id, image_large, ext, size):
    """
    Tests whether ``build_activity_asset_image_large_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_large : `None | str`
        The activity's asset's large image's value.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_large_url_as(application_id, image_large, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
