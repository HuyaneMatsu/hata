import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_small_url_as


def _iter_options():
    application_id = 202504170070
    image_small = '566666'
    yield (
        application_id,
        image_small,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.png',
    )
    
    application_id = 0
    image_small = '566666'
    yield (
        application_id,
        image_small,
        None,
        None,
        None,
    )
    
    application_id = 202504170071
    image_small = 'reisen'
    yield (
        application_id,
        image_small,
        None,
        None,
        None,
    )
    
    application_id = 202504170072
    image_small = None
    yield (
        application_id,
        image_small,
        None,
        None,
        None,
    )
    
    application_id = 202504170073
    image_small = '566666'
    yield (
        application_id,
        image_small,
        'jpg',
        128,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.jpg?size=128',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_small_url_as(application_id, image_small, ext, size):
    """
    Tests whether ``build_activity_asset_image_small_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_small : `None | str`
        The activity's asset's small image's value.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_small_url_as(application_id, image_small, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
